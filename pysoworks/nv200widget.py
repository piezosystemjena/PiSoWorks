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
    #icon.set_color(QColor.fromString(os.environ.get("QTMATERIAL_PRIMARYCOLOR", "")))
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
        ui.devicesComboBox.currentIndexChanged.connect(self.on_device_selected)
        ui.connectButton.clicked.connect(qtinter.asyncslot(self.connect_to_device))
        ui.openLoopButton.clicked.connect(qtinter.asyncslot(self.on_pid_mode_button_clicked))
        ui.closedLoopButton.clicked.connect(qtinter.asyncslot(self.on_pid_mode_button_clicked))
        
        ui.applySetpointParamButton.setIconSize(QSize(24, 24))
        ui.applySetpointParamButton.setIcon(get_icon("check", size=24, fill=True))
        ui.applySetpointParamButton.setText("Apply")
        ui.applySetpointParamButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        ui.applySetpointParamButton.setToolTip("Apply Setpoint Parameters")
        ui.applySetpointParamButton.clicked.connect(qtinter.asyncslot(self.apply_setpoint_param))

        ui.tabWidget.currentChanged.connect(qtinter.asyncslot(self.on_current_tab_changed))

        ui.consoleButton.setIcon(get_icon("terminal", size=24, fill=True))
        ui.consoleButton.setIconSize(QSize(24, 24))
        ui.consoleButton.clicked.connect(self.toggle_console_visibility)
        ui.consoleWidget.setVisible(False)
        
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

        ui.lowLevelSpinBox.valueChanged.connect(self.updateWaveformPlot)
        ui.highLevelSpinBox.valueChanged.connect(self.updateWaveformPlot)
        ui.freqSpinBox.valueChanged.connect(self.updateWaveformPlot)
        ui.phaseShiftSpinBox.valueChanged.connect(self.updateWaveformPlot)
        ui.uploadButton.clicked.connect(qtinter.asyncslot(self.upload_waveform))

        ui.console.command_entered.connect(qtinter.asyncslot(self.send_console_cmd))
        ui.console.register_commands({
            # General Commands
            "s": "Print full command list",
            "reset": "Hardware-reset of the controller",
            "fenable": "Enable/disable full range voltage sweep during power-up (0=disabled, 1=enabled)",
            "sinit": "Set initial actuator position after power-up (0 to 100 %)",
            "set": "Setpoint: voltage (open loop) or position (closed loop), range limited by actuator",
            "setst": "Smooth setpoint: setst,<value1>=Setpoint,<value2>=JumpTime; same rules as 'set'",
            "meas": "Read position (with sensor) or piezo voltage (no sensor)",
            "imeas": "Read measured piezo current (0=channel 1, 1=channel 2)",
            "ctrlmode": "Controller mode (0=PID, 1=ILC identification, 2=ILC feedforward, 3=ILC feedback)",
            "temp": "Read heat sink temperature",
            "stat": "Read status register",
            "posmin": "Lower motion range limit",
            "posmax": "Upper motion range limit",
            "avmin": "Lower voltage range limit",
            "avmax": "Upper voltage range limit",
            "modsrc": "Setpoint source (0=USB/Ethernet, 1=Analog In, 2=SPI, 3=AWG)",
            "monsrc": (
                "Analog output source (0=position closed loop, 1=setpoint, 2=piezo voltage, "
                "3=position error, 4=abs(position error), 5=position open loop, 6=piezo current 1, 7=piezo current 2)"
            ),

            # PID and Filters
            "cl": "Loop mode (0=open loop, 1=closed loop)",
            "sr": "Slew rate limit (0.0000008 to 2000.0 %/ms; 2000=disabled)",
            "kp": "PID proportional gain (0 to 10000)",
            "ki": "PID integral gain (0 to 10000)",
            "kd": "PID differential gain (0 to 10000)",
            "tf": "PID differential term (time constant)",
            "pcf": (
                "PID feedforward gain: pcf,<position_gain>,<velocity_gain>,<acceleration_gain> "
                "(acceleration scaled internally by 1/1,000,000)"
            ),
            "setlpon": "Enable/disable setpoint lowpass filter (0=off, 1=on)",
            "setlpf": "Setpoint lowpass cutoff frequency (1 to 10000 Hz)",
            "notchon": "Enable/disable notch filter (0=off, 1=on)",
            "notchf": "Notch filter frequency (1 to 10000 Hz)",
            "notchb": "Notch filter bandwidth (-3dB) (1 to 10000 Hz; max = 2 * notchf)",
            "poslpon": "Enable/disable position lowpass filter (0=off, 1=on)",
            "poslpf": "Position lowpass cutoff frequency (1 to 10000 Hz)",

            # Arbitrary Waveform Generator
            "grun": "Start/stop AWG (0=stop, 1=start)",
            "gsarb": "AWG start index (0 to 1023)",
            "gearb": "AWG end index (0 to 1023)",
            "gcarb": "AWG cycles (0=infinite, 1 to 65535)",
            "goarb": "AWG offset index (0 to 1023)",
            "giarb": "Read current AWG index",
            "gtarb": "Output sampling factor (1 to 65535; sample time = factor * 50µs)",
            "gbarb": "Write AWG buffer in % units (index: 0 to 1023, value: 0.0 to 100.0)",
            "gparb": "Write AWG buffer in length units (index: 0 to 1023, value: posmin to posmax)",
            "gsave": "Save AWG buffer to EEPROM",
            "gload": "Load AWG buffer from EEPROM",

            # Data Recorder
            "recsrc": (
                "Set data recorder source: recsrc,<ch>,<src>; ch: 0=A, 1=B; "
                "src: 0=position, 1=setpoint, 2=voltage, 3=error, 4=abs(error), "
                "5=position (open loop), 6=piezo current 1, 7=piezo current 2"
            ),
            "recast": "Recorder autostart (0=off, 1=start on set, 2=start on grun)",
            "recstr": "Recorder stride (store every nth value) (1 to 65535)",
            "reclen": "Recorder length (0 to 6144; 0=infinite loop)",
            "recrun": "Start/stop recorder (0=stop, 1=start)",
            "recidx": "Read current recorder write index",
            "recout": "Read recorder by index: recout,<ch>,<index>,<value>",
            "recoutf": "Read full recorder buffer (comma-separated)",

            # Trigger In
            "trgfkt": (
                "Trigger input function (0=none, 1=AWG start, 2=AWG step, 3=AWG sync, "
                "4=ILC sync, 5=recorder start)"
            ),

            # Trigger Out
            "trgedg": "Trigger edge mode (0=off, 1=rising, 2=falling, 3=both)",
            "trgsrc": "Trigger signal source (0=position, 1=setpoint)",
            "trgss": "Trigger start position (posmin+0.001 to posmax-0.001)",
            "trgse": "Trigger stop position (posmin+0.001 to posmax-0.001)",
            "trgsi": "Trigger step size (0.001 to posmax-0.001)",
            "trglen": "Trigger pulse length in samples (0 to 255, time = length * 50µs)",

            # SPI
            "spisrc": (
                "SPI return source (0=0x0000, 1=position, 2=setpoint, 3=voltage, 4=error, "
                "5=abs(error), 6=position open loop, 7=piezo current 1, 8=piezo current 2, 9=test 0x5A5A)"
            ),
            "spitrg": "SPI interrupt source (0=internal, 1=SPI)",
            "spis": "SPI setpoint format (0=hex, 1=decimal, 2=stroke/voltage)",

            # ILC
            "idata": "Read all ILC parameters",
            "iemin": "ILC lower error threshold 'emin' (0.0001 to 1.0)",
            "irho": "ILC learning rate 'rho' (0.0001 to 1.0)",
            "in0": "Number of basic scans (≥ in1) (2 to 65535)",
            "in1": "Number of subsamples (power of 2: 2, 4, 8...1024)",
            "inx": "Frequency components to learn (1 to 128, must be < ½ * in1)",
            "iut": "Read piezo voltage profile (time domain)",
            "iyt": "Read measured position profile (time domain)",
            "ii1t": "Read piezo current channel 1 (time domain)",
            "ii2t": "Read piezo current channel 2 (time domain)",
            "igc": "Read learning function (frequency domain)",
            "iuc": "Read piezo voltage profile (frequency domain)",
            "iwc": (
                "Set/read desired position profile (frequency domain): "
                "iwc,<index>,<real>,<imag>; index: 0 to inx"
            ),
            "iyc": "Read measured position profile (frequency domain)",
            "igt": "Correction mode (0=no learning, 1=offline ID, 2=online ID)",
            "isave": "Save ILC learning profiles to actuator",
            "iload": "Load ILC learning profiles from actuator",
        })

        self.init_modsrc_combobox()
        self.init_spimonitor_combobox()


    def init_modsrc_combobox(self):
        """
        Initializes the modsrcComboBox with available modulation sources.
        """
        cb = self.ui.modsrcComboBox
        cb.clear()
        cb.addItem("Setpoint (set cmd)", ModulationSource.SET_CMD)
        cb.addItem("Analog In", ModulationSource.ANALOG_IN)
        cb.addItem("SPI Interface", ModulationSource.SPI)
        cb.addItem("Waveform Generator", ModulationSource.WAVEFORM_GENERATOR)
        cb.activated.connect(qtinter.asyncslot(self.on_modsrc_combobox_activated))


    async def on_modsrc_combobox_activated(self, index: int):
        """
        Handles the event when a modulation source is selected from the modsrcComboBox.
        """
        if index == -1:
            print("No modulation source selected.")
            return

        source = self.ui.modsrcComboBox.itemData(index)
        if source is None:
            print("No modulation source data found.")
            return
        
        print(f"Selected modulation source: {source}")
        try:
            await self._device.set_modulation_source(source)
        except Exception as e:
            self.status_message.emit(f"Error setting modulation source: {e}", 0)

    
    def init_spimonitor_combobox(self):
        """
        Initializes the SPI monitor source combo box with available monitoring options.
        """
        cb = self.ui.spisrcComboBox
        cb.clear()
        cb.addItem("Zero (0x0000)", SPIMonitorSource.ZERO)
        cb.addItem("Closed Loop Pos.", SPIMonitorSource.CLOSED_LOOP_POS)
        cb.addItem("Setpoint", SPIMonitorSource.SETPOINT)
        cb.addItem("Piezo Voltage", SPIMonitorSource.PIEZO_VOLTAGE)
        cb.addItem("Position Error", SPIMonitorSource.ABS_POSITION_ERROR)
        cb.addItem("Open Loop Pos.", SPIMonitorSource.OPEN_LOOP_POS)
        cb.addItem("Piezo Current 1", SPIMonitorSource.PIEZO_CURRENT_1)
        cb.addItem("Piezo Current 2", SPIMonitorSource.PIEZO_CURRENT_2)
        cb.addItem("Test Value", SPIMonitorSource.TEST_VALUE)
        cb.activated.connect(qtinter.asyncslot(self.on_spimonitor_combobox_activated))


    async def on_spimonitor_combobox_activated(self, index: int):
        """
        Handles the event when a SPI monitor source is selected from the spisrcComboBox.
        """
        if index == -1:
            print("No SPI monitor source selected.")
            return

        source = self.ui.spisrcComboBox.itemData(index)
        if source is None:
            print("No SPI monitor source data found.")
            return
        
        print(f"Selected SPI monitor source: {source}")
        try:
            await self._device.set_spi_monitor_source(source)
        except Exception as e:
            self.status_message.emit(f"Error setting SPI monitor source: {e}", 0)


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
        pid_mode = PidLoopMode.CLOSED_LOOP if ui.closedLoopButton.isChecked() else PidLoopMode.OPEN_LOOP
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
            await dev.set_slew_rate(self.ui.slewRateSpinBox.value())
            await dev.set_setpoint_lowpass_filter_cutoff_freq(self.ui.setpointFilterCutoffSpinBox.value())
            await dev.enable_setpoint_lowpass_filter(self.ui.setpointFilterCheckBox.isChecked())
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
    

    async def initialize_ui_from_device(self):
        """
        Asynchronously initializes the UI elements for easy mode UI.
        """
        dev = self._device
        ui = self.ui
        pid_mode = await dev.get_pid_mode()
        if pid_mode == PidLoopMode.OPEN_LOOP:
            ui.openLoopButton.setChecked(True)
        else:
            ui.closedLoopButton.setChecked(True)
        await self.update_target_pos_edits()
        ui.targetPosSpinBox.setValue(await dev.get_setpoint())
        
    async def initialize_settings_tab_from_device(self):
        """
        Asynchronously initializes the settings tab UI elements based on the device's current settings.
        """
        dev = self._device
        ui = self.ui
        ui.slewRateSpinBox.setValue(await dev.get_slew_rate())
        ui.setpointFilterCheckBox.setChecked(await dev.is_setpoint_lowpass_filter_enabled())
        ui.setpointFilterCutoffSpinBox.setValue(await dev.get_setpoint_lowpass_filter_cutoff_freq())
        self.set_combobox_index_by_value(ui.modsrcComboBox, await dev.get_modulation_source())
        self.set_combobox_index_by_value(ui.spisrcComboBox, await dev.get_spi_monitor_source())



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
            await self.initialize_ui_from_device()
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
        if index == 1:
            print("Settings tab activated")
            await self.initialize_settings_tab_from_device()

    def updateWaveformPlot(self):
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
            print("No device connected.")
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
            await wg.set_waveform(waveform)
            print("Waveform uploaded successfully.")
            self.status_message.emit("Waveform uploaded successfully.", 2000)
        except Exception as e:
            print(f"Error uploading waveform: {e}")
            self.status_message.emit(f"Error uploading waveform: {e}", 4000)
        

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
        
        try:
            await wg.start(cycles=self.ui.cyclesSpinBox.value())
            print("Waveform generator started successfully.")
            self.status_message.emit("Waveform generator started successfully.", 2000)
        except Exception as e:
            print(f"Error starting waveform generator: {e}")
            self.status_message.emit(f"Error starting waveform generator: {e}", 4000)


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