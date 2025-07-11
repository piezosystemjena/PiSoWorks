# This Python file uses the following encoding: utf-8
import asyncio
from enum import Enum
from typing import Any, cast
import math

from PySide6.QtWidgets import QApplication, QWidget, QMenu
from PySide6.QtCore import Qt, QSize, QObject, Signal, QTimer
from PySide6.QtGui import QColor, QPalette, QAction
from PySide6.QtWidgets import QDoubleSpinBox, QComboBox
import qtinter
from matplotlib.backends.backend_qtagg import FigureCanvas
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
from nv200.waveform_generator import WaveformGenerator, WaveformType, WaveformUnit
from pysoworks.input_widget_change_tracker import InputWidgetChangeTracker
from pysoworks.svg_cycle_widget import SvgCycleWidget
from .mplcanvas import MplWidget, LightIconToolbar


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


class TabWidgetTabs(Enum):
    """
    Enumeration for the different tabs in the NV200Widget's tab widget.
    """
    EASY_MODE = 0
    SETTINGS = 1
    WAVEFORM = 2


class NV200Widget(QWidget):
    """
    Main application window for the PySoWorks UI, providing asynchronous device discovery, connection, and control features.
    Attributes:
        _device (DeviceClient): The currently connected device client, or None if not connected.
        _recorder (DataRecorder): The data recorder associated with the connected device, or None if not initialized
    """

    status_message = Signal(str, int)  # message text, timeout in ms
    DEFAULT_RECORDING_DURATION_MS : int = 120  # Default recording duration in milliseconds

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._device: NV200Device | None = None
        self._recorder : DataRecorder | None = None
        self._waveform_generator : WaveformGenerator | None = None
        self._discover_flags : DiscoverFlags = DiscoverFlags.ALL
        self._initialized = False

        self.ui = Ui_NV200Widget()
        ui = self.ui
        ui.setupUi(self)

        ui.mainProgressBar.set_duration(5000)
        ui.mainProgressBar.set_update_interval(20)
        ui.tabWidget.currentChanged.connect(qtinter.asyncslot(self.on_current_tab_changed))

        self.init_device_search_ui()
        self.init_easy_mode_ui()
        self.init_controller_param_ui()
        self.init_console_ui()
        self.init_waveform_ui()
        self.init_recorder_ui()


    @property
    def device(self) -> NV200Device:
        """
        Returns the connected device instance.

        Raises:
            RuntimeError: If no device is connected.
        """
        if not self._device:
            raise RuntimeError("Device not connected.")
        return self._device
    
    @property
    def recorder(self) -> DataRecorder:
        """
        Returns the DataRecorder instance associated with the device.
        """
        if self._recorder is None:
            self._recorder = DataRecorder(self.device)
        return self._recorder

    @property
    def waveform_generator(self) -> WaveformGenerator:
        """
        Returns the WaveformGenerator instance associated with the device.
        If it does not exist, it creates a new one.
        """
        if self._waveform_generator is None:
            self._waveform_generator = WaveformGenerator(self.device)
        return self._waveform_generator	
    

    def init_device_search_ui(self):
        """
        Initializes the device search UI components, including buttons and combo boxes for device selection.
        """
        ui = self.ui
        ui.searchDevicesButton.setIcon(get_icon("search", size=24, fill=True))
        ui.searchDevicesButton.clicked.connect(qtinter.asyncslot(self.search_all_devices))

        # Create the menu
        menu = QMenu(self)

        # Create actions
        serial_action = QAction("USB Devices", ui.searchDevicesButton)
        serial_action.setIcon(get_icon("usb"))
        ethernet_action = QAction("Ethernet Devices", ui.searchDevicesButton)
        ethernet_action.setIcon(get_icon("lan"))

        # Connect actions to appropriate slots
        serial_action.triggered.connect(qtinter.asyncslot(self.search_serial_devices))
        ethernet_action.triggered.connect(qtinter.asyncslot(self.search_ethernet_devices))

        # Add actions to menu
        menu.addAction(serial_action)
        menu.addAction(ethernet_action)

        # Set the menu to the button
        ui.searchDevicesButton.setMenu(menu)

        ui.devicesComboBox.currentIndexChanged.connect(self.on_device_selected)
        ui.connectButton.setEnabled(False)
        ui.connectButton.setIcon(get_icon("power", size=24, fill=True))
        ui.connectButton.clicked.connect(qtinter.asyncslot(self.connect_to_device))


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
        ui.console.register_commands(NV200Device.help_dict())


    def init_controller_param_ui(self):
        """
        Initializes the settings UI components for setpoint parameter application.
        """
        ui = self.ui
        ui.applyButton.setIconSize(QSize(24, 24))
        ui.applyButton.setIcon(get_icon("check", size=24, fill=True))
        ui.applyButton.clicked.connect(qtinter.asyncslot(self.apply_controller_parameters))

        ui.retrieveButton.setIconSize(QSize(24, 24))
        ui.retrieveButton.setIcon(get_icon("sync", size=24, fill=True))
        ui.retrieveButton.clicked.connect(qtinter.asyncslot(self.update_controller_ui_from_device))

        ui.restoreButton.setIconSize(QSize(24, 24))
        ui.restoreButton.setIcon(get_icon("settings_backup_restore", size=24, fill=True))

        self.init_monsrc_combobox()
        self.init_spimonitor_combobox()
        self.init_waveform_combobox()

        InputWidgetChangeTracker.register_widget_handler(
            SvgCycleWidget, "currentIndexChanged", lambda w: w.currentIndex())
        tracker = self.input_change_tracker = InputWidgetChangeTracker(self)
        for widget_type in InputWidgetChangeTracker.supported_widget_types():
            for widget in ui.controllerStructureWidget.findChildren(widget_type):
                tracker.add_widget(widget)
        
        

    def init_waveform_ui(self):
        """
        Initializes the waveform UI components for waveform generation and control.
        """
        ui = self.ui
        ui.lowLevelSpinBox.valueChanged.connect(self.update_waveform_plot)
        ui.highLevelSpinBox.valueChanged.connect(self.update_waveform_plot)
        ui.freqSpinBox.valueChanged.connect(self.update_waveform_plot)
        ui.phaseShiftSpinBox.valueChanged.connect(self.update_waveform_plot)
        ui.dutyCycleSpinBox.valueChanged.connect(self.update_waveform_plot)
        ui.uploadButton.clicked.connect(qtinter.asyncslot(self.upload_waveform))
        ui.uploadButton.setIcon(get_icon("upload", size=24, fill=True))
        ui.startWaveformButton.setIcon(get_icon("play_arrow", size=24, fill=True))
        ui.startWaveformButton.clicked.connect(qtinter.asyncslot(self.start_waveform_generator))
        ui.stopWaveformButton.setIcon(get_icon("stop", size=24, fill=True))
        ui.stopWaveformButton.clicked.connect(qtinter.asyncslot(self.stop_waveform_generator))


    def init_recorder_ui(self):
        """
        Initializes the data recorder UI components for recording and plotting data.
        """
        ui = self.ui
        ui.recDurationSpinBox.setValue(self.DEFAULT_RECORDING_DURATION_MS)
        ui.historyCheckBox.setChecked(True)
        ui.clearPlotButton.setIcon(get_icon("delete", size=24, fill=True))
        ui.clearPlotButton.clicked.connect(self.clear_waveform_plot)
        ui.freqSpinBox.valueChanged.connect(self.update_waveform_running_duration)
        ui.cyclesSpinBox.valueChanged.connect(self.update_waveform_running_duration)
        ui.recDurationSpinBox.valueChanged.connect(self.update_sampling_period)
        self.update_sampling_period()

    
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

    def init_waveform_combobox(self):
        """
        Initializes the waveform type combo box with available waveform options.
        """
        cb = self.ui.waveFormComboBox
        cb.clear()
        cb.addItem("Sine", WaveformType.SINE)
        cb.addItem("Triangle", WaveformType.TRIANGLE)
        cb.addItem("Square", WaveformType.SQUARE)
        cb.currentIndexChanged.connect(self.on_waveform_type_changed)  # Show duty cycle only for square wave
        self.on_waveform_type_changed(cb.currentIndex())  # Initialize visibility based on the current selection

    
    def on_waveform_type_changed(self, index: int):
        """
        Handles the event when the waveform type combo box is changed.
        """
        visible = (index == WaveformType.SQUARE.value)
        self.ui.dutyCycleLabel.setVisible(visible)
        self.ui.dutyCycleSpinBox.setVisible(visible)
        self.update_waveform_plot()

  
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


    async def search_all_devices(self):
        """
        Asynchronously searches for all available devices and updates the UI accordingly.
        This method is a wrapper around search_devices to allow for easy integration with other async tasks.
        """
        self._discover_flags = DiscoverFlags.ALL
        await self.search_devices()

    async def search_serial_devices(self):
        """
        Asynchronously searches for serial devices and updates the UI accordingly.
        This method is a wrapper around search_devices to allow for easy integration with other async tasks.
        """
        self._discover_flags = DiscoverFlags.DETECT_SERIAL
        await self.search_devices()

    async def search_ethernet_devices(self):
        """
        Asynchronously searches for Ethernet devices and updates the UI accordingly.
        This method is a wrapper around search_devices to allow for easy integration with other async tasks.
        """
        self._discover_flags = DiscoverFlags.DETECT_ETHERNET
        await self.search_devices()


    async def search_devices(self):
        """
        Asynchronously searches for available devices and updates the UI accordingly.
        """
        ui = self.ui
        ui.searchDevicesButton.setEnabled(False)
        ui.connectButton.setEnabled(False)
        ui.easyModeGroupBox.setEnabled(False)
        self.status_message.emit("Searching for devices...", 0)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        if self._device is not None:
            await self._device.close()
            self._device = None
        
        print("Searching...")
        ui.mainProgressBar.start(5000, "search_devices")
        try:
            print("Discovering devices...")
            devices = await discover_devices(flags=self._discover_flags | DiscoverFlags.ADJUST_COMM_PARAMS, device_class=NV200Device)    
            
            if not devices:
                print("No devices found.")
            else:
                print(f"Found {len(devices)} device(s):")
                for device in devices:
                    print(device)
            ui.mainProgressBar.stop(success=True, context="search_devices")
        except Exception as e:
            ui.mainProgressBar.reset()
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

        device = self.ui.devicesComboBox.itemData(index, role=Qt.ItemDataRole.UserRole)
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
        print("Updating target position spin boxes...")
        ui = self.ui
        setpoint_range = await self._device.get_setpoint_range()
        ui.targetPosSpinBox.setRange(setpoint_range[0], setpoint_range[1])
        ui.targetPosSpinBox.setValue(setpoint_range[1]) # Default to high end
        ui.targetPosSpinBox_2.setRange(setpoint_range[0], setpoint_range[1])
        ui.targetPosSpinBox_2.setValue(setpoint_range[0])  # Default to low end
        unit = await self._device.get_setpoint_unit()
        ui.targetPosSpinBox.setSuffix(f" {unit}")
        ui.targetPosSpinBox_2.setSuffix(f" {unit}")
        ui.targetPositionsLabel.setTextFormat(Qt.TextFormat.RichText)
        
        ui.rangeLabel.setText(f"{setpoint_range[0]:.0f} - {setpoint_range[1]:.0f} {unit}")
        ui.lowLevelSpinBox.setRange(setpoint_range[0], setpoint_range[1])
        ui.lowLevelSpinBox.setValue(setpoint_range[0])
        ui.lowLevelSpinBox.setSuffix(f" {unit}")
        ui.highLevelSpinBox.setRange(setpoint_range[0], setpoint_range[1])
        ui.highLevelSpinBox.setValue(setpoint_range[1])
        ui.highLevelSpinBox.setSuffix(f" {unit}")


    async def on_pid_mode_button_clicked(self):
        """
        Handles the event when the PID mode button is clicked.

        Determines the desired PID loop mode (closed or open loop) based on the state of the UI button,
        sends the mode to the device asynchronously, and updates the UI status bar with any errors encountered.
        """
        ui = self.ui
        pid_mode = PidLoopMode.CLOSED_LOOP if ui.closedLoopCheckBox.isChecked() else PidLoopMode.OPEN_LOOP
        try:
            await self._device.pid.set_mode(pid_mode)
            print(f"PID mode set to {pid_mode}.")
            await self.update_target_pos_edits()
        except Exception as e:
            print(f"Error setting PID mode: {e}")
            self.status_message.emit(f"Error setting PID mode: {e}", 2000)
            return
        
       
    async def apply_controller_parameters(self):
        """
        Asynchronously applies setpoint parameters to the connected device.
        """
        try:
            print("Applying scontroller parameters...")
            dev = self._device
            dirty_widgets = self.input_change_tracker.get_dirty_widgets()
            for widget in dirty_widgets:
                print(f"Applying changes from widget: {widget}")
                await widget.applyfunc(self.input_change_tracker.get_value_of_widget(widget))
                self.input_change_tracker.reset_widget(widget)
        except Exception as e:
            self.status_message.emit(f"Error setting setpoint param: {e}", 2000)


    def selected_device(self) -> DetectedDevice:
        """
        Returns the currently selected device from the devicesComboBox.
        """
        index = self.ui.devicesComboBox.currentIndex()
        if index == -1:
            return None
        return self.ui.devicesComboBox.itemData(index, role=Qt.ItemDataRole.UserRole)
    

    async def update_ui_from_device(self):
        """
        Asynchronously initializes the UI elements for easy mode UI.
        """
        print("Initializing UI from device...")
        dev = self.device
        ui = self.ui
        pid_mode = await dev.pid.get_mode()
        ui.closedLoopCheckBox.setChecked(pid_mode == PidLoopMode.CLOSED_LOOP)
        await self.update_target_pos_edits()
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
        cui.srSpinBox.applyfunc = dev.set_slew_rate

        setpoint_lpf = dev.setpoint_lpf
        cui.setlponCheckBox.setChecked(await setpoint_lpf.is_enabled())
        cui.setlponCheckBox.applyfunc = setpoint_lpf.enable
        cui.setlpfSpinBox.setMinimum(int(setpoint_lpf.cutoff_range.min))
        cui.setlpfSpinBox.setMaximum(int(setpoint_lpf.cutoff_range.max))
        cui.setlpfSpinBox.setValue(int(await setpoint_lpf.get_cutoff()))
        cui.setlpfSpinBox.applyfunc = setpoint_lpf.set_cutoff

        poslpf = dev.position_lpf
        cui.poslponCheckBox.setChecked(await poslpf.is_enabled())
        cui.poslponCheckBox.applyfunc = poslpf.enable 
        cui.poslpfSpinBox.setMinimum(poslpf.cutoff_range.min)
        cui.poslpfSpinBox.setMaximum(poslpf.cutoff_range.max)
        cui.poslpfSpinBox.setValue(await poslpf.get_cutoff())
        cui.poslpfSpinBox.applyfunc = poslpf.set_cutoff

        notch_filter = dev.notch_filter
        cui.notchonCheckBox.setChecked(await notch_filter.is_enabled())
        cui.notchonCheckBox.applyfunc = notch_filter.enable   
        cui.notchfSpinBox.setMinimum(notch_filter.freq_range.min)
        cui.notchfSpinBox.setMaximum(notch_filter.freq_range.max)  
        cui.notchfSpinBox.setValue(await notch_filter.get_frequency())
        cui.notchfSpinBox.applyfunc = notch_filter.set_frequency
        cui.notchbSpinBox.setMinimum(notch_filter.bandwidth_range.min)
        cui.notchbSpinBox.setMaximum(notch_filter.bandwidth_range.max)
        cui.notchbSpinBox.setValue(await notch_filter.get_bandwidth())
        cui.notchbSpinBox.applyfunc = notch_filter.set_bandwidth

        pid_controller = dev.pid
        pidgains = await pid_controller.get_pid_gains()
        print(f"PID Gains: {pidgains}")
        cui.kpSpinBox.setMinimum(0.0)
        cui.kpSpinBox.setMaximum(10000.0)
        cui.kpSpinBox.setSpecialValueText(cui.kpSpinBox.prefix() + "0.0 (disabled)")
        cui.kpSpinBox.setValue(pidgains.kp)
        cui.kpSpinBox.applyfunc = lambda value: pid_controller.set_pid_gains(kp=value)

        cui.kiSpinBox.setMinimum(0.0)
        cui.kiSpinBox.setMaximum(10000.0)
        cui.kiSpinBox.setSpecialValueText(cui.kpSpinBox.prefix() + "0.0 (disabled)")
        cui.kiSpinBox.setValue(pidgains.ki)
        cui.kiSpinBox.applyfunc = lambda value: pid_controller.set_pid_gains(ki=value)

        cui.kdSpinBox.setMinimum(0.0)
        cui.kdSpinBox.setMaximum(10000.0)
        cui.kdSpinBox.setSpecialValueText(cui.kdSpinBox.prefix() + "0.0 (disabled)")
        cui.kdSpinBox.setValue(pidgains.kd)
        cui.kdSpinBox.applyfunc = lambda value: pid_controller.set_pid_gains(kd=value)
        
        pcfgains = await pid_controller.get_pcf_gains()
        cui.pcfaSpinBox.setMinimum(0.0)
        cui.pcfaSpinBox.setMaximum(10000.0)
        cui.pcfaSpinBox.setSpecialValueText(cui.pcfaSpinBox.prefix() + "0.0 (disabled)")
        cui.pcfaSpinBox.setValue(pcfgains.acceleration)
        cui.pcfaSpinBox.applyfunc = lambda value: pid_controller.set_pcf_gains(acceleration=value)

        cui.pcfvSpinBox.setMinimum(0.0)
        cui.pcfvSpinBox.setMaximum(10000.0)
        cui.pcfvSpinBox.setSpecialValueText(cui.pcfvSpinBox.prefix() + "0.0 (disabled)")
        cui.pcfvSpinBox.setValue(pcfgains.velocity)
        cui.pcfvSpinBox.applyfunc = lambda value: pid_controller.set_pcf_gains(velocity=value)

        cui.pcfxSpinBox.setMinimum(0.0)
        cui.pcfxSpinBox.setMaximum(10000.0)
        cui.pcfxSpinBox.setSpecialValueText(cui.pcfxSpinBox.prefix() + "0.0 (disabled)")
        cui.pcfxSpinBox.setValue(pcfgains.position)
        cui.pcfxSpinBox.applyfunc = lambda value: pid_controller.set_pcf_gains(position=value)

        pidmode = await pid_controller.get_mode()
        cui.clToggleWidget.setCurrentIndex(pidmode.value)
        cui.clToggleWidget.applyfunc = lambda value: pid_controller.set_mode(PidLoopMode(value))

        modsrc = await dev.get_modulation_source()
        cui.modsrcToggleWidget.setCurrentIndex(modsrc.value)
        cui.modsrcToggleWidget.applyfunc = lambda value: dev.set_modulation_source(ModulationSource(value))

        self.set_combobox_index_by_value(cui.monsrcComboBox, await dev.get_analog_monitor_source())
        cui.monsrcComboBox.applyfunc = lambda value: dev.set_analog_monitor_source(AnalogMonitorSource(value))
        self.set_combobox_index_by_value(cui.spiSrcComboBox, await dev.get_spi_monitor_source())
        self.input_change_tracker.reset()
        cui.spiSrcComboBox.applyfunc = lambda value: dev.set_spi_monitor_source(SPIMonitorSource(value))
        



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
        self.setCursor(Qt.CursorShape.WaitCursor)
        detected_device = self.selected_device()
        self.status_message.emit(f"Connecting to {detected_device.identifier}...", 0)
        print(f"Connecting to {detected_device.identifier}...")
        try:
            await self.disconnect_from_device()
            self._device = cast(NV200Device, await connect_to_detected_device(detected_device))
            self.ui.easyModeGroupBox.setEnabled(True)
            await self.update_ui_from_device()
            self.status_message.emit(f"Connected to {detected_device.identifier}.", 2000)
            print(f"Connected to {detected_device.identifier}.")
        except Exception as e:
            self.status_message.emit(f"Connection failed: {e}", 2000)
            print(f"Connection failed: {e}")
            return
        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)
   

    def start_move(self):
        """
        Initiates an asynchronous move operation by creating a new asyncio task.
        """
        asyncio.create_task(self.start_move_async(self.sender()))


    async def setup_data_recorder(self, duration_ms : int = DEFAULT_RECORDING_DURATION_MS) -> DataRecorder:
        """
        Asynchronously configures the data recorder with appropriate data sources and recording duration.

        This method determines the type of position sensor used by the device and sets the first data source
        of the recorder accordingly:
            - If no position sensor type is detected, sets the first data source to SETPOINT.
            - Otherwise, sets it to PIEZO_POSITION.
        The second data source is always set to PIEZO_VOLTAGE.
        The recording duration is set to 120 milliseconds.

        Returns:
            None
        """
        dev = self.device
        recorder = self.recorder
        pos_sensor_type = await dev.get_actuator_sensor_type()
        if pos_sensor_type is None:
            await recorder.set_data_source(0, DataRecorderSource.SETPOINT)
        else:
            await recorder.set_data_source(0, DataRecorderSource.PIEZO_POSITION)
        await recorder.set_data_source(1, DataRecorderSource.PIEZO_VOLTAGE)
        await recorder.set_recording_duration_ms(duration_ms)
        return recorder


    async def plot_recorder_data(self, plot_widget: MplWidget, clear_plot: bool = True):
        """
        Asynchronously retrieves and plots recorded data from two channels.

        Emits:
            status_message (str, int): Notifies the UI about the current status.

        Raises:
            Any exceptions raised by recorder.wait_until_finished() or recorder.read_recorded_data_of_channel().
        """
        plot = plot_widget.canvas
        recorder = self.recorder
        await recorder.wait_until_finished()
        self.status_message.emit("Reading recorded data from device...", 0)
        rec_data = await recorder.read_recorded_data_of_channel(0)
        if clear_plot:
            plot.clear_plot()
        plot.add_recorder_data_line(rec_data, QColor(0, 255, 0))
        rec_data = await recorder.read_recorded_data_of_channel(1)
        plot.add_recorder_data_line(rec_data,  QColor('orange'))
        self.status_message.emit("", 0)


    async def start_move_async(self, sender: QObject):
        """
        Asynchronously starts the move operation.
        """
        try:
            dev = self.device

            spinbox : QDoubleSpinBox = sender.property("value_edit")
            ui = self.ui
            ui.easyModeGroupBox.setEnabled(False)
            ui.mainProgressBar.start(5000, "start_move")

            recorder = await self.setup_data_recorder()
            await recorder.set_autostart_mode(RecorderAutoStartMode.START_ON_SET_COMMAND)
            await recorder.start_recording()

            # Implement the move logic here
            # For example, you might want to send a command to the device to start moving.
            # await self._device.start_move()
            print("Starting move operation...")
            await dev.move(spinbox.value())
            self.status_message.emit("Move operation started.", 0)
            await self.plot_recorder_data(ui.easyModePlot)
            ui.mainProgressBar.stop(success=True, context="start_move")
        except Exception as e:
            self.status_message.emit(f"Error during move operation: {e}", 4000)
            ui.mainProgressBar.reset()
            print(f"Error during move operation: {e}")
            return
        finally:
            ui.easyModeGroupBox.setEnabled(True)
            self.status_message.emit("", 0)

    async def on_current_tab_changed(self, index: int):
        """
        Handles the event when the current tab in the tab widget is changed.
        """
        self.ui.stackedWidget.setCurrentIndex(index)
        if index == TabWidgetTabs.SETTINGS.value:
            print("Settings tab activated")
            await self.update_controller_ui_from_device()
        elif index == TabWidgetTabs.WAVEFORM.value:
            print("Waveform tab activated")
            self.update_waveform_plot()


    def current_waveform_type(self) -> WaveformType:
        """
        Returns the currently selected waveform type from the waveform combo box.
        """
        cb = self.ui.waveFormComboBox
        return cb.currentData(role=Qt.ItemDataRole.UserRole)   


    def update_waveform_plot(self):
        """
        Updates the waveform plot in the UI when the corresponding tab is active.
        """
        ui = self.ui
        if ui.tabWidget.currentIndex() != TabWidgetTabs.WAVEFORM.value:
            return
        
        print("Updating waveform plot...")
        waveform = WaveformGenerator.generate_waveform(
            waveform_type=self.current_waveform_type(),
            low_level=ui.lowLevelSpinBox.value(),
            high_level=ui.highLevelSpinBox.value(),
            freq_hz=ui.freqSpinBox.value(),
            phase_shift_rad=math.radians(ui.phaseShiftSpinBox.value()),
            duty_cycle=ui.dutyCycleSpinBox.value() / 100.0
        )
        plot = ui.waveformPlot.canvas
        line_count = plot.get_line_count()
        if line_count == 0:
            plot.plot_data(waveform.sample_times_ms, waveform.values, "Waveform", QColor("#02cfff"))
        else:
            plot.update_line(0, waveform.sample_times_ms, waveform.values)

        # Adjust the plot axes based on the waveform data if it does not contain any history lines
        if line_count <= 1:
            offset = (ui.highLevelSpinBox.value() - ui.lowLevelSpinBox.value()) * 0.01
            plot.scale_axes(0, 1000, ui.lowLevelSpinBox.minimum() - offset, ui.highLevelSpinBox.maximum() + offset)



    async def upload_waveform(self):
        """
        Asynchronously uploads the waveform to the device.
        """
        try:
            wg = self.waveform_generator
            waveform = WaveformGenerator.generate_waveform(
                waveform_type=self.current_waveform_type(),
                low_level=self.ui.lowLevelSpinBox.value(),
                high_level=self.ui.highLevelSpinBox.value(),
                freq_hz=self.ui.freqSpinBox.value(),
                phase_shift_rad=math.radians(self.ui.phaseShiftSpinBox.value()),
                duty_cycle=self.ui.dutyCycleSpinBox.value() / 100.0
            )
            self.setCursor(Qt.CursorShape.WaitCursor)
            unit = WaveformUnit.POSITION if self.ui.closedLoopCheckBox.isChecked() else WaveformUnit.VOLTAGE
            await wg.set_waveform(waveform, unit=unit, on_progress=self.report_progress)
            self.status_message.emit("Waveform uploaded successfully.", 2000)
        except Exception as e:
            self.status_message.emit(f"Error uploading waveform: {e}", 4000)
        finally:#
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.ui.mainProgressBar.reset()
        
    def fade_plot_line(self, line_index: int, alpha: float = 0.5):
        """
        Fades the specified plot line by reducing its alpha value.
        
        Args:
            line_index (int): The index of the line to fade.
            alpha (float): The alpha value to set for the line (0.0 to 1.0).
        """
        plot = self.ui.waveformPlot.canvas
        color = plot.get_line_color(line_index)
        color.setAlphaF(color.alphaF() * alpha)
        plot.set_line_color(line_index, color)


    async def plot_waveform_recorder_data(self):
        """
        Plots waveform recorder data on the UI's matplotlib canvas.

        If the 'history' checkbox is checked, previous plot lines (except the first) are faded.
        Otherwise, the waveform plot is cleared before plotting new data.
        Finally, recorder data is plotted.
        """
        ui = self.ui
        plot = ui.waveformPlot.canvas
        if ui.historyCheckBox.isChecked():
            for i in range(1, plot.get_line_count()):
                self.fade_plot_line(i)
        else:
            self.clear_waveform_plot()
        await self.plot_recorder_data(plot_widget=ui.waveformPlot, clear_plot=False)


    async def start_waveform_generator(self):
        """
        Asynchronously starts the waveform generator.
        """       
        ui = self.ui
        try:
            wg = self.waveform_generator
            ui.mainProgressBar.start(5000, "start_waveform")

            recorder = await self.setup_data_recorder(ui.recDurationSpinBox.value())
            await recorder.set_autostart_mode(RecorderAutoStartMode.START_ON_WAVEFORM_GEN_RUN)
            await recorder.start_recording()

            ui.startWaveformButton.setEnabled(False)
            await wg.start(cycles=self.ui.cyclesSpinBox.value())
            print("Waveform generator started successfully.")
            self.status_message.emit("Waveform generator started successfully.", 2000)
            
            await self.plot_waveform_recorder_data()

            ui.mainProgressBar.stop(success=True, context="start_waveform")
            await wg.wait_until_finished()
        except Exception as e:
            print(f"Error starting waveform generator: {e}")
            self.status_message.emit(f"Error starting waveform generator: {e}", 4000)
            ui.mainProgressBar.reset()
        finally:
            ui.startWaveformButton.setEnabled(True)


    async def stop_waveform_generator(self):
        """
        Asynchronously stops the waveform generator.
        """        
        try:
            wg = self.waveform_generator
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
        ui.mainProgressBar.setMaximum(total)
        ui.mainProgressBar.setValue(current_index)
        self.status_message.emit(f" Uploading waveform - sample {current_index} of {total} [{percent:.1f}%]", 0)


    def showEvent(self, event):
        """
        Handles the widget's show event. Ensures initialization logic is executed only once
        when the widget is shown for the first time. Schedules an asynchronous search for
        serial devices unsing QTimer after the widget is displayed.

        Args:
            event (QShowEvent): The event object associated with the widget being shown.
        """
        super().showEvent(event)
        if self._initialized:
            return

        self._initialized = True
        QTimer.singleShot(0, qtinter.asyncslot(self.search_serial_devices))
        ui = self.ui
        ui.scrollArea.setFixedWidth(ui.scrollArea.widget().sizeHint().width() + 40)  # +40 for scroll bar width

    
    def clear_waveform_plot(self):
        """
        Clears the waveform plot in the UI.
        """
        plot = self.ui.waveformPlot.canvas
        plot.clear_plot()
        self.update_waveform_plot()


    def update_sampling_period(self):
        """
        Updates the sampling period in the waveform generator based on the given value.

        Args:
            value (int): The new sampling period in milliseconds.
        """
        ui = self.ui
        sample_period = DataRecorder.get_sample_period_ms_for_duration(ui.recDurationSpinBox.value())
        ui.samplePeriodSpinBox.setValue(sample_period)



    def update_waveform_running_duration(self,):
        """
        Updates the waveform running duration in the waveform generator based on the given value.

        Args:
            value (int): The new running duration in milliseconds.
        """
        ui = self.ui
        freq_hz = ui.freqSpinBox.value()
        cycles = ui.cyclesSpinBox.value()
        duration_ms = 1000 * cycles / freq_hz if freq_hz > 0 else 0.0
        ui.waveformDurationSpinBox.setValue(int(duration_ms))

