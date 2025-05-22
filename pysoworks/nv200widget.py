# This Python file uses the following encoding: utf-8
import sys
import asyncio
import logging
import os

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QDir, QCoreApplication, QSize, QObject, Signal
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QDoubleSpinBox
import qtinter
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from nv200.device_types import DetectedDevice, PidLoopMode, DiscoverFlags
from nv200.device_discovery import discover_devices
from nv200.device_interface import DeviceClient, create_device_client
from nv200.data_recorder import DataRecorder, DataRecorderSource, RecorderAutoStartMode
from qt_material import apply_stylesheet
from pathlib import Path
from qt_material_icons import MaterialIcon


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_nv200widget import Ui_NV200Widget


def get_icon(icon_name: str, size: int = 24, fill: bool = True) -> MaterialIcon:
    icon = MaterialIcon(icon_name, size=size, fill=fill)
    icon.set_color(QColor.fromString(os.environ.get("QTMATERIAL_PRIMARYCOLOR", "")))
    return icon



class NV200Widget(QWidget):
    """
    Main application window for the PySoWorks UI, providing asynchronous device discovery, connection, and control features.
    Attributes:
        _device (DeviceClient): The currently connected device client, or None if not connected.
        _recorder (DataRecorder): The data recorder associated with the connected device, or None if not initialized
    """

    _device: DeviceClient = None
    _recorder : DataRecorder = None
    status_message = Signal(str, int)  # message text, timeout in ms

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_NV200Widget()
        ui = self.ui
        ui.setupUi(self)
        ui.searchDevicesButton.clicked.connect(qtinter.asyncslot(self.search_devices))
        ui.devicesComboBox.currentIndexChanged.connect(self.on_device_selected)
        ui.connectButton.clicked.connect(qtinter.asyncslot(self.connect_to_device))
        ui.openLoopButton.clicked.connect(qtinter.asyncslot(self.on_pid_mode_button_clicked))
        ui.closedLoopButton.clicked.connect(qtinter.asyncslot(self.on_pid_mode_button_clicked))
        ui.slewRateSpinBox.editingFinished.connect(qtinter.asyncslot(self.on_slow_rate_editing_finished))
        ui.moveProgressBar.set_duration(5000)
        ui.moveProgressBar.set_update_interval(20)

        ui.moveButton.setIcon(get_icon("play_arrow", size=24, fill=True))
        ui.moveButton.setStyleSheet("QPushButton { padding: 0px }")
        ui.moveButton.setIconSize(QSize(24, 24))
        ui.moveButton.clicked.connect(self.start_move)
        ui.moveButton.setProperty("value_edit", ui.targetPosSpinBox)

        ui.moveButton_2.setIcon(ui.moveButton.icon())
        ui.moveButton_2.setStyleSheet("QPushButton { padding: 0px }")
        ui.moveButton_2.setIconSize(ui.moveButton.iconSize())
        ui.moveButton_2.clicked.connect(self.start_move)
        ui.moveButton_2.setProperty("value_edit", ui.targetPosSpinBox_2)
        self.setWindowTitle("PySoWorks")

    async def search_devices(self):
        """
        Asynchronously searches for available devices and updates the UI accordingly.
        """
        ui = self.ui
        ui.searchDevicesButton.setEnabled(False)
        ui.connectButton.setEnabled(False)
        ui.easyModeGroupBox.setEnabled(False)
        self.status_message.emit("Searching for devices...", 0)
        QApplication.setOverrideCursor(Qt.WaitCursor)

        if self._device is not None:
            await self._device.close()
            self._device = None
        
        print("Searching...")
        ui.moveProgressBar.start(5000, "search_devices")
        try:
            print("Discovering devices...")
            devices = await discover_devices(flags=DiscoverFlags.ALL)    
            
            if not devices:
                print("No devices found.")
            else:
                print(f"Found {len(devices)} device(s):")
                for device in devices:
                    print(device)
            ui.moveProgressBar.stop(success=True, context="search_devices")
        except Exception as e:
            ui.moveProgressBar.reset()
            print(f"Error: {e}")
        finally:
            QApplication.restoreOverrideCursor()
            self.ui.searchDevicesButton.setEnabled(True)
            self.status_message.emit("", 0)
            print("Search completed.")
            self.ui.devicesComboBox.clear()
            if devices:
                for device in devices:
                    self.ui.devicesComboBox.addItem(f"{device}", device)
            else:
                self.ui.devicesComboBox.addItem("No devices found.")
            
            
    def on_device_selected(self, index):
        """
        Handles the event when a device is selected from the devicesComboBox.
        """
        if index == -1:
            print("No device selected.")
            return

        device = self.ui.devicesComboBox.itemData(index, role=Qt.UserRole)
        if device is None:
            print("No device data found.")
            return
        
        print(f"Selected device: {device}")
        self.ui.connectButton.setEnabled(True)


    async def on_pid_mode_button_clicked(self):
        """
        Handles the event when the PID mode button is clicked.

        Determines the desired PID loop mode (closed or open loop) based on the state of the UI button,
        sends the mode to the device asynchronously, and updates the UI status bar with any errors encountered.
        """
        ui = self.ui
        pid_mode = PidLoopMode.CLOSED_LOOP if ui.closedLoopButton.isChecked() else PidLoopMode.OPEN_LOOP
        try:
            await self._device.set_pid_mode(pid_mode)
            print(f"PID mode set to {pid_mode}.")
        except Exception as e:
            print(f"Error setting PID mode: {e}")
            self.status_message.emit(f"Error setting PID mode: {e}", 2000)
            return
        
    async def on_slow_rate_editing_finished(self):
        """
        Handles the event when the slew rate editing is finished.

        Sends the new slew rate to the device asynchronously and updates the UI status bar with any errors encountered.
        """
        ui = self.ui
        try:
            await self._device.set_slew_rate(ui.slewRateSpinBox.value())
            print(f"Slew rate set to {ui.slewRateSpinBox.value()}.")
        except Exception as e:
            print(f"Error setting slew rate: {e}")
            self.status_message.emit(f"Error setting slew rate: {e}", 2000)
            return


    def selected_device(self) -> DetectedDevice:
        """
        Returns the currently selected device from the devicesComboBox.
        """
        index = self.ui.devicesComboBox.currentIndex()
        if index == -1:
            return None
        return self.ui.devicesComboBox.itemData(index, role=Qt.UserRole)
    

    async def initialize_easy_mode_ui(self):
        """
        Asynchronously initializes the UI elements for easy mode UI.
        """
        dev = self._device
        ui = self.ui
        ui.targetPosSpinBox.setValue(await dev.get_setpoint())
        pid_mode = await dev.get_pid_mode()
        if pid_mode == PidLoopMode.OPEN_LOOP:
            ui.openLoopButton.setChecked(True)
        else:
            ui.closedLoopButton.setChecked(True)
        ui.slewRateSpinBox.setValue(await dev.get_slew_rate())
        ui.setpointFilterCheckBox.setChecked(await dev.is_setpoint_lowpass_filter_enabled())
        ui.setpointFilterCutoffSpinBox.setValue(await dev.get_setpoint_lowpass_filter_cutoff_freq())


    async def disconnect_from_device(self):
        """
        Asynchronously disconnects from the currently connected device.
        """
        if self._device is None:
            print("No device connected.")
            return

        await self._device.close()
        self._device = None       
        self._recorder = None
            


    async def connect_to_device(self):
        """
        Asynchronously connects to the selected device.
        """
        detected_device = self.selected_device()
        self.status_message.emit(f"Connecting to {detected_device.identifier}...", 2000)
        print(f"Connecting to {detected_device.identifier}...")
        try:
            await self.disconnect_from_device()
            self._device = create_device_client(detected_device)
            await self._device.connect()
            self.ui.easyModeGroupBox.setEnabled(True)
            await self.initialize_easy_mode_ui()
            self.status_message.emit(f"Connected to {detected_device.identifier}.", 2000)
            print(f"Connected to {detected_device.identifier}.")
        except Exception as e:
            self.status_message.emit(f"Connection failed: {e}", 2000)
            print(f"Connection failed: {e}")
            return


    def recorder(self) -> DataRecorder:
        """
        Returns the DataRecorder instance associated with the device.
        """
        if self._device is None:
            return None

        if self._recorder is None:
            self._recorder = DataRecorder(self._device)
        return self._recorder	
    

    def start_move(self):
        """
        Initiates an asynchronous move operation by creating a new asyncio task.
        """
        asyncio.create_task(self.start_move_async(self.sender()))


    async def start_move_async(self, sender: QObject):
        """
        Asynchronously starts the move operation.
        """
        if self._device is None:
            print("No device connected.")
            return
        
        spinbox : QDoubleSpinBox = sender.property("value_edit")
        ui = self.ui
        ui.easyModeGroupBox.setEnabled(False)
        ui.moveProgressBar.start(5000, "start_move")
        try:
            recorder = self.recorder()
            await recorder.set_data_source(0, DataRecorderSource.PIEZO_POSITION)
            await recorder.set_data_source(1, DataRecorderSource.PIEZO_VOLTAGE)
            await recorder.set_autostart_mode(RecorderAutoStartMode.START_ON_SET_COMMAND)
            await recorder.set_recording_duration_ms(120)
            await recorder.start_recording()

            # Implement the move logic here
            # For example, you might want to send a command to the device to start moving.
            # await self._device.start_move()
            print("Starting move operation...")
            await self._device.move(spinbox.value())
            self.status_message.emit("Move operation started.", 0)
            await recorder.wait_until_finished()
            self.status_message.emit("Reading recorded data from device...", 0)
            rec_data = await recorder.read_recorded_data_of_channel(0)
            ui.mplCanvasWidget.canvas.plot_data(rec_data, QColor(0, 255, 0))
            rec_data = await recorder.read_recorded_data_of_channel(1)
            ui.mplCanvasWidget.canvas.add_line(rec_data,  QColor('orange'))
            ui.moveProgressBar.stop(success=True, context="start_move")
        except Exception as e:
            self.status_message.emit(f"Error during move operation: {e}", 4000)
            ui.moveProgressBar.reset()
            print(f"Error during move operation: {e}")
            return
        finally:
            ui.easyModeGroupBox.setEnabled(True)
            self.status_message.emit("", 0)

