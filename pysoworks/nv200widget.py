# This Python file uses the following encoding: utf-8
import sys
import asyncio
import logging
import os
from typing import Any, Tuple
import math

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QDir, QCoreApplication, QSize, QObject, Signal
from PySide6.QtGui import QColor, QIcon, QPalette
from PySide6.QtWidgets import QDoubleSpinBox, QComboBox
import qtinter
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from qt_material import apply_stylesheet
from pathlib import Path
from qt_material_icons import MaterialIcon

from nv200.shared_types import (
    DetectedDevice,
    PidLoopMode,
    DiscoverFlags,
    ModulationSource,
    SPIMonitorSource,
    AnalogMonitorSource
)
from nv200.device_discovery import discover_devices
from nv200.nv200_device import NV200Device
from nv200.data_recorder import DataRecorder, DataRecorderSource, RecorderAutoStartMode
from nv200.connection_utils import connect_to_detected_device
from nv200.waveform_generator import WaveformGenerator


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from pysoworks.ui_nv200widget import Ui_NV200Widget


def get_icon(icon_name: str, size: int = 24, fill: bool = True, color : QPalette.ColorRole = QPalette.ColorRole.Highlight) -> MaterialIcon:
    """
    Creates and returns a MaterialIcon object with the specified icon name, size, fill style, and color.

    Args:
        icon_name (str): The name of the icon to retrieve.
        size (int, optional): The size of the icon in pixels. Defaults to 24.
        fill (bool, optional): Whether the icon should be filled or outlined. Defaults to True.
        color (QPalette.ColorRole, optional): The color role to use for the icon. Defaults to QPalette.ColorRole.Highlight.
    """
    icon = MaterialIcon(icon_name, size=size, fill=fill)
    icon.set_color(QPalette().color(color))
    return icon



class NV200Widget(QWidget):
    """
    Main application window for the PySoWorks UI, providing asynchronous device discovery, connection, and control features.
    Attributes:
        _device (DeviceClient): The currently connected device client, or None if not connected.
        _recorder (DataRecorder): The data recorder associated with the connected device, or None if not initialized
    """

    status_message = Signal(str, int)  # message text, timeout in ms

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._device: NV200Device | None = None
        self._recorder : DataRecorder | None = None
        self._waveform_generator : WaveformGenerator | None = None

        self.ui = Ui_NV200Widget()
        ui = self.ui
        ui.setupUi(self)

        ui.searchDevicesButton.clicked.connect(qtinter.asyncslot(self.search_devices))
        ui.searchDevicesButton.setIcon(get_icon("search", size=24, fill=True))
        ui.devicesComboBox.currentIndexChanged.connect(self.on_device_selected)
        ui.connectButton.clicked.connect(qtinter.asyncslot(self.connect_to_device))
        ui.connectButton.setIcon(get_icon("power", size=24, fill=True))
        ui.moveProgressBar.set_duration(5000)
        ui.moveProgressBar.set_update_interval(20)

        self.init_easy_mode_ui()
        self.init_settings_ui()
        self.init_console_ui()
        self.init_waveform_ui()
        ui.tabWidget.currentChanged.connect(qtinter.asyncslot(self.on_current_tab_changed))

    def init_easy_mode_ui(self):
        """
        Initializes the easy mode UI components, including buttons and spin boxes for PID control and target position.
        """
        ui = self.ui
        ui.closedLoopCheckBox.clicked.connect(qtinter.asyncslot(self.on_pid_mode_button_clicked))
    
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

        ui.closedLoopCheckBox.toggled.connect(
            (lambda checked: ui.closedLoopCheckBox.setText("Closed Loop" if checked else "Open Loop"))
        )



    def init_console_ui(self):
        """
        Initializes the console UI with a prompt and command history.
        """
        ui = self.ui
        ui.consoleButton.setIcon(get_icon("terminal", size=24, fill=True))
        ui.consoleButton.setIconSize(QSize(24, 24))
        ui.consoleButton.clicked.connect(self.toggle_console_visibility)
        ui.consoleWidget.setVisible(False)
        ui.console.command_entered.connect(qtinter.asyncslot(self.send_console_cmd))
        ui.console.register_commands(NV200Device.help_dict)

    def init_settings_ui(self):
        """
        Initializes the settings UI components for setpoint parameter application.
        """
        ui = self.ui
        ui.applyButton.setIconSize(QSize(24, 24))
        ui.applyButton.setIcon(get_icon("check", size=24, fill=True))
        ui.applyButton.clicked.connect(qtinter.asyncslot(self.apply_setpoint_param))

        ui.retrieveButton.setIconSize(QSize(24, 24))
        ui.retrieveButton.setIcon(get_icon("sync", size=24, fill=True))
        ui.retrieveButton.clicked.connect(qtinter.asyncslot(self.update_controller_ui_from_device))

        ui.restoreButton.setIconSize(QSize(24, 24))
        ui.restoreButton.setIcon(get_icon("settings_backup_restore", size=24, fill=True))

        
        # ui.setpointFilterCheckBox.toggled.connect(
        #     (lambda checked: ui.setpointFilterCheckBox.setText("LP Filter ON" if checked else "LP Filter OFF"))
        # )
        self.init_monsrc_combobox()
        self.init_spimonitor_combobox()


    def init_waveform_ui(self):
        """
        Initializes the waveform UI components for waveform generation and control.
        """
        ui = self.ui
        ui.lowLevelSpinBox.valueChanged.connect(self.updateWaveformPlot)
        ui.highLevelSpinBox.valueChanged.connect(self.updateWaveformPlot)
        ui.freqSpinBox.valueChanged.connect(self.updateWaveformPlot)
        ui.phaseShiftSpinBox.valueChanged.connect(self.updateWaveformPlot)
        ui.uploadButton.clicked.connect(qtinter.asyncslot(self.upload_waveform))
        ui.uploadButton.setIcon(get_icon("upload", size=24, fill=True))
        ui.startWaveformButton.setIcon(get_icon("play_arrow", size=24, fill=True))
        ui.startWaveformButton.clicked.connect(qtinter.asyncslot(self.start_waveform_generator))
        ui.stopWaveformButton.setIcon(get_icon("stop", size=24, fill=True))
        ui.stopWaveformButton.clicked.connect(qtinter.asyncslot(self.stop_waveform_generator))

    
    def init_spimonitor_combobox(self):
        """
        Initializes the SPI monitor source combo box with available monitoring options.
        """
        cb = self.ui.controllerStructureWidget.ui.spiSrcComboBox
        cb.clear()
        cb.addItem("Zero (0x0000)", SPIMonitorSource.ZERO)
        cb.addItem("Closed Loop Pos.", SPIMonitorSource.CLOSED_LOOP_POS)
        cb.addItem("Setpoint", SPIMonitorSource.SETPOINT)
        cb.addItem("Piezo Voltage", SPIMonitorSource.PIEZO_VOLTAGE)
        cb.addItem("Position Error", SPIMonitorSource.ABS_POSITION_ERROR)
        cb.addItem("Open Loop Pos.", SPIMonitorSource.OPEN_LOOP_POS)
        cb.addItem("Piezo Current 1", SPIMonitorSource.PIEZO_CURRENT_1)
        cb.addItem("Piezo Current 2", SPIMonitorSource.PIEZO_CURRENT_2)
        cb.addItem("Test Value (0x5a5a)", SPIMonitorSource.TEST_VALUE_0x5A5A)

    def init_monsrc_combobox(self):
        """
        Initializes the modsrcComboBox with available modulation sources.
        """
        cb = self.ui.controllerStructureWidget.ui.monsrcComboBox
        cb.clear()
        cb.addItem("Closed Loop Pos.", AnalogMonitorSource.CLOSED_LOOP_POS)
        cb.addItem("Setpoint", AnalogMonitorSource.SETPOINT)
        cb.addItem("Piezo Voltage", AnalogMonitorSource.PIEZO_VOLTAGE)
        cb.addItem("Position Error", AnalogMonitorSource.ABS_POSITION_ERROR)
        cb.addItem("Open Loop Pos.", AnalogMonitorSource.OPEN_LOOP_POS)
        cb.addItem("Piezo Current 1", AnalogMonitorSource.PIEZO_CURRENT_1)
        cb.addItem("Piezo Current 2", AnalogMonitorSource.PIEZO_CURRENT_2)
  

    def set_combobox_index_by_value(self, combobox: QComboBox, value: Any) -> None:
        """
        Sets the current index of a QComboBox based on the given userData value.

        :param combobox: The QComboBox to modify.
        :param value: The value to match against the item userData.
        """
        index = combobox.findData(value)
        if index != -1:
            combobox.setCurrentIndex(index)
        else:
            # Optional: Log or raise if not found
            print(f"Warning: Value {value} not found in combobox.")


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
            devices = await discover_devices(flags=DiscoverFlags.ALL | DiscoverFlags.ADJUST_COMM_PARAMS, device_class=NV200Device)    
            
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

    async def update_target_pos_edits(self):
        """
        Asynchronously updates the minimum and maximum values for the target position spin boxes
        in the UI based on the setpoint range retrieved from the device.
        """
        ui = self.ui
        setpoint_range = await self._device.get_setpoint_range()
        ui.targetPosSpinBox.setRange(setpoint_range[0], setpoint_range[1])
        ui.targetPosSpinBox_2.setRange(setpoint_range[0], setpoint_range[1])
        unit = await self._device.get_setpoint_unit()
        ui.targetPosSpinBox.setSuffix(f" {unit}")
        ui.targetPosSpinBox_2.setSuffix(f" {unit}")
        ui.targetPositionsLabel.setTextFormat(Qt.TextFormat.RichText)
        ui.rangeLabel.setText(f"{setpoint_range[0]:.0f} - {setpoint_range[1]:.0f} {unit}")
        ui.lowLevelSpinBox.setRange(setpoint_range[0], setpoint_range[1])
        ui.lowLevelSpinBox.setValue(setpoint_range[0])
        ui.highLevelSpinBox.setRange(setpoint_range[0], setpoint_range[1])
        ui.highLevelSpinBox.setValue(setpoint_range[1])


    async def on_pid_mode_button_clicked(self):
        """
        Handles the event when the PID mode button is clicked.

        Determines the desired PID loop mode (closed or open loop) based on the state of the UI button,
        sends the mode to the device asynchronously, and updates the UI status bar with any errors encountered.
        """
        ui = self.ui
        pid_mode = PidLoopMode.CLOSED_LOOP if ui.closedLoopCheckBox.isChecked() else PidLoopMode.OPEN_LOOP
        try:
            await self._device.set_pid_mode(pid_mode)
            print(f"PID mode set to {pid_mode}.")
            await self.update_target_pos_edits()
        except Exception as e:
            print(f"Error setting PID mode: {e}")
            self.status_message.emit(f"Error setting PID mode: {e}", 2000)
            return
        
       
    async def apply_setpoint_param(self):
        """
        Asynchronously applies setpoint parameters to the connected device.
        """
        try:
            print("Applying setpoint parameters...")
            dev = self._device
            # await dev.set_slew_rate(self.ui.slewRateSpinBox.value())
            # await dev.set_setpoint_lowpass_filter_cutoff_freq(self.ui.setpointFilterCutoffSpinBox.value())
            # await dev.enable_setpoint_lowpass_filter(self.ui.setpointFilterCheckBox.isChecked())
        except Exception as e:
            self.status_message.emit(f"Error setting setpoint param: {e}", 2000)


    def selected_device(self) -> DetectedDevice:
        """
        Returns the currently selected device from the devicesComboBox.
        """
        index = self.ui.devicesComboBox.currentIndex()
        if index == -1:
            return None
        return self.ui.devicesComboBox.itemData(index, role=Qt.UserRole)
    

    async def update_ui_from_device(self):
        """
        Asynchronously initializes the UI elements for easy mode UI.
        """
        print("Initializing UI from device...")
        dev = self._device
        ui = self.ui
        pid_mode = await dev.get_pid_mode()
        ui.closedLoopCheckBox.setChecked(pid_mode == PidLoopMode.CLOSED_LOOP)
        await self.update_target_pos_edits()
        ui.targetPosSpinBox.setValue(await dev.get_setpoint())
        await self.update_controller_ui_from_device()
        


    async def update_controller_ui_from_device(self):
        """
        Asynchronously initializes the controller settings UI elements based on the device's current settings.
        """
        dev = self._device
        if dev is None:
            print("No device connected.")
            return
        
        print("Initializing controller settings from device...")
        ui = self.ui
        cui = ui.controllerStructureWidget.ui
        cui.srSpinBox.setMinimum(0.0000008)
        cui.srSpinBox.setMaximum(2000)
        cui.srSpinBox.setValue(await dev.get_slew_rate())

        setpoint_lpf = dev.setpoint_lpf
        cui.setlponCheckBox.setChecked(await setpoint_lpf.is_enabled())
        cui.setlpfSpinBox.setMinimum(int(setpoint_lpf.cutoff_range.min))
        cui.setlpfSpinBox.setMaximum(int(setpoint_lpf.cutoff_range.max))
        cui.setlpfSpinBox.setValue(int(await setpoint_lpf.get_cutoff()))

        poslpf = dev.position_lpf
        cui.poslponCheckBox.setChecked(await poslpf.is_enabled())
        cui.poslpfSpinBox.setMinimum(poslpf.cutoff_range.min)
        cui.poslpfSpinBox.setMaximum(poslpf.cutoff_range.max)
        cui.poslpfSpinBox.setValue(await poslpf.get_cutoff())

        notch_filter = dev.notch_filter
        cui.notchonCheckBox.setChecked(await notch_filter.is_enabled())
        cui.notchfSpinBox.setMinimum(notch_filter.freq_range.min)
        cui.notchfSpinBox.setMaximum(notch_filter.freq_range.max)  
        cui.notchfSpinBox.setValue(await notch_filter.get_frequency())
        cui.notchbSpinBox.setMinimum(notch_filter.bandwidth_range.min)
        cui.notchbSpinBox.setMaximum(notch_filter.bandwidth_range.max)
        cui.notchbSpinBox.setValue(await notch_filter.get_bandwidth())

        pidgains = await dev.get_pid_gains()
        print(f"PID Gains: {pidgains}")
        cui.kpSpinBox.setMinimum(0.0)
        cui.kpSpinBox.setMaximum(10000.0)
        cui.kpSpinBox.setSpecialValueText(cui.kpSpinBox.prefix() + "0.0 (disabled)")
        cui.kpSpinBox.setValue(pidgains.kp)

        cui.kiSpinBox.setMinimum(0.0)
        cui.kiSpinBox.setMaximum(10000.0)
        cui.kiSpinBox.setSpecialValueText(cui.kpSpinBox.prefix() + "0.0 (disabled)")
        cui.kiSpinBox.setValue(pidgains.ki)

        cui.kdSpinBox.setMinimum(0.0)
        cui.kdSpinBox.setMaximum(10000.0)
        cui.kdSpinBox.setSpecialValueText(cui.kpSpinBox.prefix() + "0.0 (disabled)")
        cui.kdSpinBox.setValue(pidgains.kd)
        
        pcfgains = await dev.get_pcf_gains()
        cui.pcfaSpinBox.setMinimum(0.0)
        cui.pcfaSpinBox.setMaximum(10000.0)
        cui.pcfaSpinBox.setSpecialValueText(cui.pcfaSpinBox.prefix() + "0.0 (disabled)")
        cui.pcfaSpinBox.setValue(pcfgains.acceleration)

        cui.pcfvSpinBox.setMinimum(0.0)
        cui.pcfvSpinBox.setMaximum(10000.0)
        cui.pcfvSpinBox.setSpecialValueText(cui.pcfvSpinBox.prefix() + "0.0 (disabled)")
        cui.pcfvSpinBox.setValue(pcfgains.velocity)

        cui.pcfxSpinBox.setMinimum(0.0)
        cui.pcfxSpinBox.setMaximum(10000.0)
        cui.pcfxSpinBox.setSpecialValueText(cui.pcfxSpinBox.prefix() + "0.0 (disabled)")
        cui.pcfxSpinBox.setValue(pcfgains.position)

        pidmode = await dev.get_pid_mode()
        cui.clToggleWidget.setCurrent(pidmode.value)

        modsrc = await dev.get_modulation_source()
        cui.modsrcToggleWidget.setCurrent(modsrc.value)

        self.set_combobox_index_by_value(cui.monsrcComboBox, await dev.get_analog_monitor_source())
        self.set_combobox_index_by_value(cui.spiSrcComboBox, await dev.get_spi_monitor_source())
        



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
        self.setCursor(Qt.WaitCursor)
        detected_device = self.selected_device()
        self.status_message.emit(f"Connecting to {detected_device.identifier}...", 0)
        print(f"Connecting to {detected_device.identifier}...")
        try:
            await self.disconnect_from_device()
            self._device = await connect_to_detected_device(detected_device)
            self.ui.easyModeGroupBox.setEnabled(True)
            await self.update_ui_from_device()
            self.status_message.emit(f"Connected to {detected_device.identifier}.", 2000)
            print(f"Connected to {detected_device.identifier}.")
        except Exception as e:
            self.status_message.emit(f"Connection failed: {e}", 2000)
            print(f"Connection failed: {e}")
            return
        finally:
            self.setCursor(Qt.ArrowCursor)

    def recorder(self) -> DataRecorder| None:
        """
        Returns the DataRecorder instance associated with the device.
        """
        if self._device is None:
            return None

        if self._recorder is None:
            self._recorder = DataRecorder(self._device)
        return self._recorder	
    
    def waveform_generator(self) -> WaveformGenerator | None:
        """
        Returns the WaveformGenerator instance associated with the device.
        If it does not exist, it creates a new one.
        """
        if self._device is None:
            return None

        if self._waveform_generator is None:
            self._waveform_generator = WaveformGenerator(self._device)
        return self._waveform_generator
    

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
            ui.mplCanvasWidget.canvas.plot_recorder_data(rec_data, QColor(0, 255, 0))
            rec_data = await recorder.read_recorded_data_of_channel(1)
            ui.mplCanvasWidget.canvas.add_recorder_data_line(rec_data,  QColor('orange'))
            ui.moveProgressBar.stop(success=True, context="start_move")
        except Exception as e:
            self.status_message.emit(f"Error during move operation: {e}", 4000)
            ui.moveProgressBar.reset()
            print(f"Error during move operation: {e}")
            return
        finally:
            ui.easyModeGroupBox.setEnabled(True)
            self.status_message.emit("", 0)

    async def on_current_tab_changed(self, index: int):
        """
        Handles the event when the current tab in the tab widget is changed.
        """
        self.ui.stackedWidget.setCurrentIndex(1 if index == 1 else 0)
        if index == 1:
            print("Settings tab activated")
            await self.update_controller_ui_from_device()


    def updateWaveformPlot(self):
        """
        Updates the waveform plot in the UI when the corresponding tab is active.
        """
        if self.ui.tabWidget.currentIndex() != 2:
            return
        
        print("Updating waveform plot...")
        waveform = WaveformGenerator.generate_sine_wave(
            low_level=self.ui.lowLevelSpinBox.value(),
            high_level=self.ui.highLevelSpinBox.value(),
            freq_hz=self.ui.freqSpinBox.value(),
            phase_shift_rad=math.radians(self.ui.phaseShiftSpinBox.value())
        )
        ui = self.ui
        mpl_canvas = self.ui.mplCanvasWidget.canvas
        mpl_canvas.plot_data(waveform.sample_times_ms, waveform.values, "Waveform", QColor(0, 255, 150))
        mpl_canvas.scale_axes(0, 1000, 0, 80)


    async def upload_waveform(self):
        """
        Asynchronously uploads the waveform to the device.
        """
        if self._device is None:
            self.status_message.emit("Error: No device connected", 4000)
            return
        
        wg = self.waveform_generator()
        if wg is None:
            print("Waveform generator not initialized.")
            return
        
        waveform = WaveformGenerator.generate_sine_wave(
            low_level=self.ui.lowLevelSpinBox.value(),
            high_level=self.ui.highLevelSpinBox.value(),
            freq_hz=self.ui.freqSpinBox.value(),
            phase_shift_rad=math.radians(self.ui.phaseShiftSpinBox.value())
        )
        
        try:
            self.setCursor(Qt.WaitCursor)
            await wg.set_waveform(waveform, on_progress=self.report_progress)
            self.status_message.emit("Waveform uploaded successfully.", 2000)
        except Exception as e:
            self.status_message.emit(f"Error uploading waveform: {e}", 4000)
        finally:#
            self.setCursor(Qt.ArrowCursor)
            self.ui.moveProgressBar.reset()
        

    async def start_waveform_generator(self):
        """
        Asynchronously starts the waveform generator.
        """
        if self._device is None:
            print("No device connected.")
            return
        
        wg = self.waveform_generator()
        if wg is None:
            print("Waveform generator not initialized.")
            return
        
        ui = self.ui
        try:
            ui.startWaveformButton.setEnabled(False)
            await wg.start(cycles=self.ui.cyclesSpinBox.value())
            print("Waveform generator started successfully.")
            self.status_message.emit("Waveform generator started successfully.", 2000)
            await wg.wait_until_finished()
        except Exception as e:
            print(f"Error starting waveform generator: {e}")
            self.status_message.emit(f"Error starting waveform generator: {e}", 4000)
        finally:
            ui.startWaveformButton.setEnabled(True)


    async def stop_waveform_generator(self):
        """
        Asynchronously stops the waveform generator.
        """
        if self._device is None:
            print("No device connected.")
            return
        
        wg = self.waveform_generator()
        if wg is None:
            print("Waveform generator not initialized.")
            return
        
        try:
            await wg.stop()
            print("Waveform generator stopped successfully.")
            self.status_message.emit("Waveform generator stopped successfully.", 2000)
        except Exception as e:
            print(f"Error stopping waveform generator: {e}")
            self.status_message.emit(f"Error stopping waveform generator: {e}", 4000)


    async def send_console_cmd(self, command: str):
        """
        Sends a command to the connected device and handles the response.
        """
        print(f"Sending command: {command}")
        # if command == "cl,0":
        #     self.ui.console.print_output("response")
        # return

        if self._device is None:
            print("No device connected.")
            return
        
        self.ui.console.prompt_count += 1
        response = await self._device.read_stripped_response_string(command, 10)
        print(f"Command response: {response}")
        self.ui.console.print_output(response)


    def toggle_console_visibility(self):
        """
        Toggles the visibility of the console widget.
        """
        if self.ui.consoleWidget.isVisible():
            self.ui.consoleWidget.hide()
        else:
            self.ui.consoleWidget.show()

    async def report_progress(self, current_index: int, total: int):
        """
        Asynchronously updates the progress bar and status message to reflect the current progress of an upload operation.

        Args:
            current_index (int): The current item index being processed.
            total (int): The total number of items to process.
        """
        percent = 100 * current_index / total
        ui = self.ui
        ui.moveProgressBar.setMaximum(total)
        ui.moveProgressBar.setValue(current_index)
        self.status_message.emit(f" Uploading waveform - sample {current_index} of {total} [{percent:.1f}%]", 0)
