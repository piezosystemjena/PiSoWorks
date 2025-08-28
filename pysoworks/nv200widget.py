# This Python file uses the following encoding: utf-8
from pathlib import Path
import asyncio
from enum import Enum
import pandas as pd

from typing import Any, cast, Dict, Tuple, List
import math
import numpy as np

from PySide6.QtWidgets import QApplication, QWidget, QMenu, QFileDialog
from PySide6.QtCore import Qt, QSize, QObject, Signal, QTimer, QStandardPaths, QUrl
from PySide6.QtGui import QColor, QPalette, QAction, QPixmap, QDesktopServices
from PySide6.QtWidgets import QDoubleSpinBox, QComboBox, QMessageBox
import qtinter

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.widgets import Cursor
from matplotlib.font_manager import FontProperties
import matplotlib as mpl

from qt_material_icons import MaterialIcon

from nv200.shared_types import (
    DetectedDevice,
    PidLoopMode,
    DiscoverFlags,
    ModulationSource,
    SPIMonitorSource,
    AnalogMonitorSource,
    PostionSensorType
)
from nv200.device_discovery import discover_devices
from nv200.nv200_device import NV200Device
from nv200.data_recorder import DataRecorder, DataRecorderSource, RecorderAutoStartMode
from nv200.connection_utils import connect_to_detected_device
from nv200.waveform_generator import WaveformGenerator, WaveformType, WaveformUnit
from nv200.analysis import ResonanceAnalyzer
from nv200.utils import DeviceParamFile
from pysoworks.input_widget_change_tracker import InputWidgetChangeTracker
from pysoworks.svg_cycle_widget import SvgCycleWidget
from pysoworks.mplcanvas import MplWidget, MplCanvas
from pysoworks.ui_helpers import get_icon, get_icon_for_menu, set_combobox_index_by_value, safe_asyncslot, repolish, images_path
import pysoworks.ui_helpers as ui_helpers
from pysoworks.action_manager import ActionManager, MenuID, action_manager
from pysoworks.style_manager import StyleManager, style_manager


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from pysoworks.ui_nv200widget import Ui_NV200Widget



class TabWidgetTabs(Enum):
    """
    Enumeration for the different tabs in the NV200Widget's tab widget.
    """
    EASY_MODE = 0
    SETTINGS = 1
    WAVEFORM = 2
    RESONANCE = 3


class NV200Widget(QWidget):
    """
    Main application window for the PySoWorks UI, providing asynchronous device discovery, connection, and control features.
    Attributes:
        _device (DeviceClient): The currently connected device client, or None if not connected.
        _recorder (DataRecorder): The data recorder associated with the connected device, or None if not initialized
    """

    status_message = Signal(str, int)  # message text, timeout in ms
    DEFAULT_RECORDING_DURATION_MS : int = 120  # Default recording duration in milliseconds
    browse_dev_param_action : QAction | None = None

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._device: NV200Device | None = None
        self._recorder : DataRecorder | None = None
        self._waveform_generator : WaveformGenerator | None = None
        self._analyzer : ResonanceAnalyzer | None = None
        self._discover_flags : DiscoverFlags = DiscoverFlags.ALL
        self._initialized = False
        self._rec_chan0 : DataRecorder.ChannelRecordingData
        self._rec_chan1 : DataRecorder.ChannelRecordingData
        self.settings_widget_change_tracker: InputWidgetChangeTracker = InputWidgetChangeTracker(self)
        self.waveform_widget_change_tracker: InputWidgetChangeTracker = InputWidgetChangeTracker(self)
        self._last_waveform_freq_hz: float = 1.0
        self._hysteresis_rec_cycles: int = 1  # number of recorded cycles for hysteresis measurement
        self._controller_param_widgets: Dict[str, QWidget] = {}
        self._custom_waveform: WaveformGenerator.WaveformData = WaveformGenerator.WaveformData() # empty list
   
        self.ui = Ui_NV200Widget()

        qt_font = self.font()
        font_family = qt_font.family()
        print(f"Font Family: {font_family}")
        font_size = qt_font.pointSizeF()
        #mpl.rcParams['font.family'] = font_family
        mpl.rcParams['font.size'] = font_size

        ui = self.ui
        ui.setupUi(self)

        ui.tabWidget.setCurrentIndex(TabWidgetTabs.EASY_MODE.value)
        ui.stackedWidget.setCurrentIndex(TabWidgetTabs.EASY_MODE.value)
        ui.tabWidget.currentChanged.connect(safe_asyncslot(self.on_current_tab_changed))

        self.init_device_search_ui()
        self.init_easy_mode_ui()
        self.init_controller_param_ui()
        self.init_console_ui()
        self.init_waveform_ui()
        self.init_recorder_ui()
        self.init_resonance_ui()

        self.set_ui_connected(False)
        self.register_main_menu_actions()
        self.set_piezosystem_logo(style_manager.style.is_current_theme_dark())
        style_manager.style.dark_mode_changed.connect(self.set_piezosystem_logo)


    def cleanup(self):
        """
        Cleans up resources by initiating an asynchronous disconnection from the device.
        This function needs to get called, before the widget is deleted
        """
        result = asyncio.create_task(self.disconnect_from_device())



    def set_piezosystem_logo(self, dark_theme : bool):
        """
        Sets the piezosystem logo on the UI based on the selected theme.

        Args:
            dark_theme (bool): If True, sets the logo for dark theme; otherwise, sets the logo for light theme.

        Side Effects:
            Updates the pixmap of the piezoIconLabel in the UI to display the appropriate logo image.
        """
        self.ui.piezoIconLabel.setPixmap(ui_helpers.company_logo_pixmap(dark_theme))


    def register_main_menu_actions(self):
        """
        Registers the main menu actions with the ActionManager.
        This method should be called after the main window is initialized.
        """
        if NV200Widget.browse_dev_param_action is not None:
            return

        NV200Widget.browse_dev_param_action = a = QAction("Browse Device Parameter Backups ...", self.parentWidget())
        a.setIcon(ui_helpers.get_icon_for_menu("folder", size=24, fill=False))
        action_manager.add_action_to_menu(MenuID.FILE, a)
        a.triggered.connect(self.browse_device_param_backups)


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
    def is_device_connected(self) -> bool:
        """
        Checks if a device is currently connected.

        Returns:
            bool: True if a device is connected, False otherwise.
        """
        return self._device is not None
    
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
    

    @property
    def analyzer(self) -> ResonanceAnalyzer:
        """
        Returns the ResonanceAnalyzer instance associated with the device.
        If it does not exist, it creates a new one.
        """
        if self._analyzer is None:
            self._analyzer = ResonanceAnalyzer(self.device)
        return self._analyzer
    

    def set_ui_connected(self, connected: bool):
        """
        Enables or disables the tab widget in the UI based on the connection status.

        Args:
            connected (bool): If True, enables the tab widget; if False, disables it.
        """
        ui = self.ui
        ui.tabWidget.setEnabled(connected)
    

    def init_device_search_ui(self):
        """
        Initializes the device search UI components, including buttons and combo boxes for device selection.
        """
        ui = self.ui
        ui.searchDevicesButton.setIcon(get_icon("search", size=24, fill=True))
        ui.searchDevicesButton.clicked.connect(safe_asyncslot(self.search_all_devices))

        # Create the menu
        menu = QMenu(self)

        # Create actions
        serial_action = QAction("USB Devices", ui.searchDevicesButton)
        serial_action.setIcon(get_icon_for_menu("usb"))
        ethernet_action = QAction("Ethernet Devices", ui.searchDevicesButton)
        ethernet_action.setIcon(get_icon("lan"))

        # Connect actions to appropriate slots
        serial_action.triggered.connect(safe_asyncslot(self.search_serial_devices))
        ethernet_action.triggered.connect(safe_asyncslot(self.search_ethernet_devices))

        # Add actions to menu
        menu.addAction(serial_action)
        menu.addAction(ethernet_action)

        # Set the menu to the button
        ui.searchDevicesButton.setMenu(menu)

        ui.devicesComboBox.currentIndexChanged.connect(self.on_device_selected)
        ui.connectButton.setEnabled(False)
        ui.connectButton.setIcon(get_icon("power", size=24, fill=True))
        ui.connectButton.clicked.connect(safe_asyncslot(self.connect_to_device))


    def init_easy_mode_ui(self):
        """
        Initializes the easy mode UI components, including buttons and spin boxes for PID control and target position.
        """
        ui = self.ui
        ui.closedLoopCheckBox.clicked.connect(safe_asyncslot(self.on_pid_mode_button_clicked))
    
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
        ui.easyModePlot.show_export_action()
        style_manager.style.dark_mode_changed.connect(ui.easyModePlot.set_dark_mode)



    def init_console_ui(self):
        """
        Initializes the console UI with a prompt and command history.
        """
        ui = self.ui
        ui.consoleButton.setIcon(get_icon("terminal", size=24, fill=True))
        ui.consoleButton.setIconSize(QSize(24, 24))
        ui.consoleButton.clicked.connect(self.toggle_console_visibility)
        ui.consoleWidget.setVisible(False)
        ui.console.command_entered.connect(safe_asyncslot(self.send_console_cmd))
        ui.console.register_commands(NV200Device.help_dict())


    def init_controller_param_ui(self):
        """
        Initializes the settings UI components for setpoint parameter application.
        """
        ui = self.ui
        ui.applyButton.setIconSize(QSize(24, 24))
        ui.applyButton.setIcon(get_icon("check", size=24, fill=True))
        ui.applyButton.clicked.connect(safe_asyncslot(self.apply_controller_parameters))

        ui.retrieveButton.setIconSize(QSize(24, 24))
        ui.retrieveButton.setIcon(get_icon("sync", size=24, fill=True))
        ui.retrieveButton.clicked.connect(safe_asyncslot(self.update_controller_ui_from_device))

        ui.restorePrevButton.setIconSize(QSize(24, 24))
        ui.restorePrevButton.setIcon(get_icon("arrow_back", size=24, fill=True))
        ui.restorePrevButton.clicked.connect(safe_asyncslot(self.restore_previous_settings))

        ui.restoreInitialButton.setIconSize(QSize(24, 24))
        ui.restoreInitialButton.setIcon(get_icon("replay", size=24, fill=True))
        ui.restoreInitialButton.clicked.connect(safe_asyncslot(self.restore_initial_settings))

        ui.exportSettingsButton.setIconSize(QSize(24, 24))
        ui.exportSettingsButton.setIcon(get_icon("save", size=24, fill=True))
        ui.exportSettingsButton.clicked.connect(safe_asyncslot(self.export_controller_param))

        ui.loadSettingsButton.setIconSize(QSize(24, 24))
        ui.loadSettingsButton.setIcon(get_icon("folder_open", size=24, fill=True))
        ui.loadSettingsButton.clicked.connect(safe_asyncslot(self.load_controller_param))

        ui.restoreDefaultButton.setIconSize(QSize(24, 24))
        ui.restoreDefaultButton.setIcon(get_icon("settings_backup_restore", size=24, fill=True))
        ui.restoreDefaultButton.clicked.connect(safe_asyncslot(self.restore_default_settings))

        self.init_monsrc_combobox()
        self.init_spimonitor_combobox()
        self.init_waveform_combobox()

        InputWidgetChangeTracker.register_widget_handler(
            SvgCycleWidget, "currentIndexChanged", lambda w: w.get_current_index(), lambda w, v: w.set_current_index(int(v)))
        tracker = self.settings_widget_change_tracker
        for widget_type in InputWidgetChangeTracker.supported_widget_types():
            for widget in ui.controllerStructureWidget.findChildren(widget_type):
                tracker.add_widget(widget)

        # Assign commands to controller structure widgets for parameter export / import
        cui = ui.controllerStructureWidget.ui
        prop_name = "cmd"
        cui.srSpinBox.setProperty(prop_name, "sr")
        cui.setlponCheckBox.setProperty(prop_name, "setlpon")
        cui.setlpfSpinBox.setProperty(prop_name, "setlpf")

        cui.poslponCheckBox.setProperty(prop_name, "poslpon")
        cui.poslpfSpinBox.setProperty(prop_name, "poslpf")

        cui.notchonCheckBox.setProperty(prop_name, "notchon")
        cui.notchfSpinBox.setProperty(prop_name, "notchf")
        cui.notchbSpinBox.setProperty(prop_name, "notchb")

        cui.kpSpinBox.setProperty(prop_name, "kp")
        cui.kiSpinBox.setProperty(prop_name, "ki")
        cui.kdSpinBox.setProperty(prop_name, "kd")
        
        cui.pcfaSpinBox.setProperty(prop_name, "pcf")
        cui.pcfaSpinBox.export_func = lambda: f"{cui.pcfxSpinBox.value()},{cui.pcfvSpinBox.value()},{cui.pcfaSpinBox.value()}"

        
        def restore_pcf_func(s):
            """
            Small helper function to restore the pcf values from a string.
            """
            try:
                values = [float(v) for v in s.split(",")]
                cui.pcfxSpinBox.setValue(int(values[0]))
                cui.pcfvSpinBox.setValue(int(values[1]))
                cui.pcfaSpinBox.setValue(int(values[2]))
            except (ValueError, IndexError) as e:
                print(f"Restore failed: {e}")

        cui.pcfaSpinBox.restore_func = restore_pcf_func

        cui.clToggleWidget.setProperty(prop_name, "cl")
        cui.modsrcToggleWidget.setProperty(prop_name, "modsrc")
        cui.monsrcComboBox.setProperty(prop_name, "monsrc")
        cui.spiSrcComboBox.setProperty(prop_name, "mspisrc")

        parent = cui.srSpinBox.parentWidget()
        for child in parent.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly):
            if child.property("cmd") is not None:
                cmd_value = str(child.property("cmd"))
                self._controller_param_widgets[cmd_value] = child

            
        

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
        ui.uploadButton.clicked.connect(self.on_upload_waveform_button_clicked)
        ui.uploadButton.setIcon(get_icon("upload", size=24, fill=True))
        ui.startWaveformButton.setIcon(get_icon("play_arrow", size=24, fill=True))
        ui.startWaveformButton.clicked.connect(safe_asyncslot(self.start_waveform_generator))
        ui.stopWaveformButton.setIcon(get_icon("stop", size=24, fill=True))
        ui.stopWaveformButton.clicked.connect(safe_asyncslot(self.stop_waveform_generator))
        ui.plotHysteresisButton.clicked.connect(self.plot_hysteresis)
        ui.measureHysteresisButton.clicked.connect(safe_asyncslot(self.measure_hysteresis))
        ui.freqSpinBox.valueChanged.connect(self.update_waveform_running_duration)
        ui.cyclesSpinBox.valueChanged.connect(self.update_waveform_running_duration)
        ui.waveSamplingPeriodSpinBox.valueChanged.connect(self.update_waveform_running_duration)
        ui.recSyncCheckBox.clicked.connect(self.sync_waveform_recording_duration)
        ui.importButton.clicked.connect(self.import_custom_waveform)
        self.update_waveform_running_duration()
        self.sync_waveform_recording_duration()

        tracker = self.waveform_widget_change_tracker
        tracker.add_widget(ui.waveFormComboBox)
        tracker.add_widget(ui.freqSpinBox)
        tracker.add_widget(ui.phaseShiftSpinBox)
        tracker.add_widget(ui.dutyCycleSpinBox)
        tracker.add_widget(ui.lowLevelSpinBox)
        tracker.add_widget(ui.highLevelSpinBox)

        tracker.set_all_widgets_dirty()  # set all widgets to dirty initially
        tracker.dirtyStateChanged.connect(self.update_waveform_run_controls)

        #setup waveform plot
        plot = ui.waveformPlot.canvas
        plot.set_plot_title("Data Recorder")

        # setup hysteresis plot
        plot = ui.hysteresisPlot.canvas
        ax = plot.ax1
        rec_ui = ui.waveformPlot.ui
        ax.set_xlabel(rec_ui.recsrc1ComboBox.currentData())
        ax.set_ylabel(rec_ui.recsrc2ComboBox.currentData())
        plot.set_plot_title("Hysteresis")
        ui.hysteresisPlot.show_export_action()

        style_manager.style.dark_mode_changed.connect(ui.waveformPlot.mpl_widget.set_dark_mode)
        style_manager.style.dark_mode_changed.connect(ui.hysteresisPlot.set_dark_mode)


    def update_waveform_run_controls(self, dirty: bool = False):
        """
        Updates the enabled state of waveform run control buttons based on the current state of waveform widgets.

        Disables the 'Start Waveform' and 'Measure Hysteresis' buttons if any waveform widget has unsaved changes.
        Enables the buttons if all widgets are in a clean state.
        """
        #enable = not dirty
        enable = True  # Always enable for now
        ui = self.ui
        ui.startWaveformButton.setEnabled(enable)
        ui.measureHysteresisButton.setEnabled(enable)



    def init_recorder_ui(self):
        """
        Initializes the data recorder UI components for recording and plotting data.
        """
        self.ui.waveformPlot.clear_plot_action.triggered.connect(self.clear_waveform_plot)


    def init_resonance_ui(self):
        """
        Initializes the resonance test UI components.
        """
        ui = self.ui
        ui.resonanceButton.setIcon(get_icon("equalizer", size=24, fill=True))
        ui.resonanceButton.setIconSize(QSize(24, 24))
        ui.resonanceButton.clicked.connect(safe_asyncslot(self.get_resonance_spectrum))
        ax = ui.resonancePlot.canvas.ax1
        ax.set_title("Resonance Spectrum")
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Amplitude') 
        ax.set_xlim(10, 4000)

        ax = ui.impulsePlot.canvas.ax1
        ax.set_title("Impulse Response")
        style_manager.style.dark_mode_changed.connect(ui.impulsePlot.set_dark_mode)
        style_manager.style.dark_mode_changed.connect(ui.resonancePlot.set_dark_mode)
        ui.impulsePlot.show_export_action()
        ui.resonancePlot.show_export_action()

    
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
        cb.addItem("Custom", -1)
        cb.currentIndexChanged.connect(self.on_waveform_type_changed)  # Show duty cycle only for square wave
        self.on_waveform_type_changed(cb.currentIndex())  # Initialize visibility based on the current selection

    
    def on_waveform_type_changed(self, index: int):
        """
        Handles the event when the waveform type combo box is changed.
        """
        ui = self.ui
        duty_visible = (index == WaveformType.SQUARE.value)
        ui.dutyCycleLabel.setVisible(duty_visible)
        ui.dutyCycleSpinBox.setVisible(duty_visible)

        is_custom = (index == (WaveformType.SQUARE.value + 1))
        ui.customLabel.setVisible(is_custom)
        ui.importButton.setVisible(is_custom)

        ui.freqLabel.setVisible(not is_custom)
        ui.freqSpinBox.setVisible(not is_custom)
        ui.waveSamplingPeriodSpinBox.setReadOnly(not is_custom)
        if ui.waveSamplingPeriodSpinBox.isReadOnly():
            ui.waveSamplingPeriodSpinBox.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        else:
            ui.waveSamplingPeriodSpinBox.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.UpDownArrows)
        repolish(ui.waveSamplingPeriodSpinBox)
        ui.phaseLabel.setVisible(not is_custom)
        ui.phaseShiftSpinBox.setVisible(not is_custom)
        ui.highLabel.setVisible(not is_custom)
        ui.highLevelSpinBox.setVisible(not is_custom)
        ui.lowLabel.setVisible(not is_custom)
        ui.lowLevelSpinBox.setVisible(not is_custom)

        self.update_waveform_plot()


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
        self.status_message.emit("Searching for devices...", 0)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
       
        print("Searching...")
        ui.mainProgressBar.start(3000)
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
        dev = self.device

        setpoint_range = await dev.get_setpoint_range()
        ui.targetPosSpinBox.setRange(setpoint_range[0], setpoint_range[1])
        ui.targetPosSpinBox.setValue(setpoint_range[1]) # Default to high end
        ui.targetPosSpinBox_2.setRange(setpoint_range[0], setpoint_range[1])
        ui.targetPosSpinBox_2.setValue(setpoint_range[0])  # Default to low end
        unit = await dev.get_setpoint_unit()
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
            await self.device.pid.set_mode(pid_mode)
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
            print("Applying controller parameters...")
            tracker = self.settings_widget_change_tracker
            tracker.backup_initial_values("previous")
            dirty_widgets = tracker.get_dirty_widgets()
            for widget in dirty_widgets:
                print(f"Applying changes from widget: {widget}")
                await widget.applyfunc(tracker.get_value_of_widget(widget))
                tracker.reset_widget(widget)
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
    

    async def init_ui_from_device(self):
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
        self.settings_widget_change_tracker.backup_current_values("initial")
        self.settings_widget_change_tracker.backup_current_values("previous")
        await self.update_resonance_ui_from_device()
        await self.update_resonance_voltages_ui()


    async def update_resonance_ui_from_device(self):
        """
        Asynchronously updates the y-axis labels of the impulse and resonance plots in the UI
        based on the device's position sensor and unit.

        If the device has a position sensor, retrieves the position unit from the device and
        updates the y-axis labels accordingly. Otherwise, defaults to "A" as the unit.

        The impulse plot's y-axis label is set to "Value (<unit>)".
        The resonance plot's y-axis label is set to "Amplitude (<unit>)".
        """
        dev = self.device
        impulse_resp_unit = "A"
        y_label = "Piezo Current (A)"
        if await dev.has_position_sensor():
            impulse_resp_unit = await dev.get_position_unit()
            y_label = f"Piezo Position ({impulse_resp_unit})"
        ax = self.ui.impulsePlot.canvas.ax1
        ax.set_ylabel(y_label)
        ax = self.ui.resonancePlot.canvas.ax1
        ax.set_ylabel(f"Amplitude ({impulse_resp_unit})")


    async def update_resonance_voltages_ui(self):
        """
        Asynchronously updates the resonance voltages in the UI based on the device's current settings.
        """
        analyzer = self.analyzer
        ui = self.ui
        
        try:
            baseline_v, impulse_v = await analyzer.get_impulse_voltages()
            ui.impulseBaseVoltageSpinBox.setValue(baseline_v)
            ui.impulsePeakVoltageSpinBox.setValue(impulse_v)
        except Exception as e:
            print(f"Error updating resonance voltages: {e}")
            self.status_message.emit(f"Error updating resonance voltages: {e}", 2000)
        


    async def update_controller_ui_from_device(self):
        """
        Asynchronously initializes the controller settings UI elements based on the device's current settings.
        """
        dev = self.device
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
        cui.pcfxSpinBox.setMaximum(1)
        cui.pcfxSpinBox.setSpecialValueText(cui.pcfxSpinBox.prefix() + "0.0 (disabled)")
        cui.pcfxSpinBox.setValue(pcfgains.position)
        cui.pcfxSpinBox.applyfunc = lambda value: pid_controller.set_pcf_gains(position=value)

        pidmode = await pid_controller.get_mode()
        cui.clToggleWidget.set_current_index(pidmode.value)
        cui.clToggleWidget.applyfunc = lambda value: pid_controller.set_mode(PidLoopMode(value))

        modsrc = await dev.get_modulation_source()
        cui.modsrcToggleWidget.set_current_index(modsrc.value)
        cui.modsrcToggleWidget.applyfunc = lambda value: dev.set_modulation_source(ModulationSource(value))

        set_combobox_index_by_value(cui.monsrcComboBox, await dev.get_analog_monitor_source())
        cui.monsrcComboBox.applyfunc = lambda value: dev.set_analog_monitor_source(AnalogMonitorSource(value))
        set_combobox_index_by_value(cui.spiSrcComboBox, await dev.get_spi_monitor_source())
        self.settings_widget_change_tracker.reset()
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
        self._waveform_generator = None
        self._analyzer = None  
            


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
            self.set_ui_connected(False)
            self._device = cast(NV200Device, await connect_to_detected_device(detected_device))
            await self.backup_actuator_config()
            self.ui.easyModeGroupBox.setEnabled(True)

            self._recorder = DataRecorder(self._device)
            self._waveform_generator = WaveformGenerator(self._device)
            self._analyzer = ResonanceAnalyzer(self._device)

            self.set_ui_connected(True)
            await self.init_ui_from_device()
            self.status_message.emit(f"Connected to {detected_device.identifier}.", 2000)
            print(f"Connected to {detected_device.identifier}.")
        except Exception as e:
            self.status_message.emit(f"Connection failed: {e}", 2000)
            print(f"Connection failed: {e}")
            return
        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)


    def actuator_backup_path(self) -> Path:
        """
        Returns the backup directory path for actuator configurations.

        The path is constructed by retrieving the user's Documents location,
        appending the application name, and then the 'actuator_configs' folder.

        Returns:
            Path: The full path to the actuator backup directory.
        """
        documents_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        app_name = QApplication.applicationName()
        backup_dir = Path(documents_path) / app_name / "actuator_configs"
        return backup_dir


    async def actuator_backup_filepath(self) -> Path:
        """
        Asynchronously generates the backup file path for the actuator configuration.
        """
        dev = self.device
        filename = await dev.default_actuator_export_filename()
        return self.actuator_backup_path() / filename


    async def backup_actuator_config(self):
        """
        Asynchronously backs up the current actuator configuration to a file.
        
        This method retrieves the current actuator configuration from the device and saves it to a file.
        The file is named with the device's serial number and the current timestamp.
        """
        try:
            backup_path = await self.actuator_backup_filepath()
            print(f"Backup path: {backup_path}")
            if backup_path.exists():
                print("Backup already exists. Skipping backup.")
                return  # or return True / some status indicator
            dev = self.device
            await dev.export_actuator_config(filepath=str(backup_path))
        except Exception as e:
            self.status_message.emit(f"Error backing up actuator config: {e}", 2000)
   

    def start_move(self):
        """
        Initiates an asynchronous move operation by creating a new asyncio task.
        """
        asyncio.create_task(self.start_move_async(self.sender()))

    async def setup_data_recorder(
        self,
        duration_ms: int = DEFAULT_RECORDING_DURATION_MS,
        recsrc0: DataRecorderSource | None = None,
        recsrc1: DataRecorderSource | None = None,
    ) -> DataRecorder:
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
        if recsrc0 is None:
            recsrc0 = DataRecorderSource.PIEZO_VOLTAGE
        if recsrc1 is None:
            pos_sensor_type = await dev.get_actuator_sensor_type()
            if pos_sensor_type is PostionSensorType.NONE:
                recsrc1 = DataRecorderSource.SETPOINT
            else:
                recsrc1 = DataRecorderSource.PIEZO_POSITION
 
        await recorder.set_data_source(0, recsrc0)
        await recorder.set_data_source(1, recsrc1)
        await recorder.set_recording_duration_ms(duration_ms)
        return recorder


    async def plot_recorder_data(self, plot_widget: MplWidget, clear_plot: bool = True, second_axes_index = 0) -> Tuple[DataRecorder.ChannelRecordingData, DataRecorder.ChannelRecordingData]:
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
        rec_data0 = await recorder.read_recorded_data_of_channel(0)
        if clear_plot:
            plot.clear_plot()
        plot.add_recorder_data_line(rec_data0, QColor('orange'), 0)
        rec_data1 = await recorder.read_recorded_data_of_channel(1)
        plot.add_recorder_data_line(rec_data1, QColor(0, 255, 0), second_axes_index)
        self.status_message.emit("", 0)
        return rec_data0, rec_data1


    def ask_upload_waveform(self) -> bool:
        """
        Prompts the user with a dialog asking whether to upload waveform data to the device.

        Returns:
            bool: True if the user chooses 'Yes' to upload the waveform, False otherwise.
        """
        reply = QMessageBox.question(
            self.parent(),
            "Upload Waveform",
            "Waveform data has not been uploaded to the device yet.\n\nShould it be uploaded now?",
            QMessageBox.Yes | QMessageBox.No
        )
        return reply == QMessageBox.Yes
    

    async def ensure_waveform_uploaded(self) -> bool:
        """
        Ensures that the waveform data is uploaded to the device before proceeding with any operations.

        Returns:
            bool: True if the waveform was successfully uploaded, False if the user cancelled the upload.
        """
        if not self.waveform_widget_change_tracker.has_dirty_widgets():
            return True

        if self.ask_upload_waveform():
            await self.upload_waveform()
            return True
        else:
            print("Waveform upload cancelled by user.")
            return False


    async def measure_hysteresis(self): 
        """
        Measures hysteresis by configuring the UI and starting the waveform generator.

        - Sets the number of cycles to 3 in the UI.
        - Selects recording sources for the waveform plot based on whether closed-loop mode is enabled:
            - If closed-loop: records setpoint and piezo position.
            - If open-loop: records piezo voltage and piezo position.
        - Initiates the waveform generator asynchronously.
        """
        if not await self.ensure_waveform_uploaded():
            return

        ui = self.ui
        ui.cyclesSpinBox.setValue(3)  # Set cycles to 3 for hysteresis measurement
        self._hysteresis_rec_cycles = ui.cyclesSpinBox.value()
        if ui.closedLoopCheckBox.isChecked():
            ui.waveformPlot.set_recording_source(0, DataRecorderSource.SETPOINT)
            ui.waveformPlot.set_recording_source(1, DataRecorderSource.PIEZO_POSITION)
        else:  
            ui.waveformPlot.set_recording_source(0, DataRecorderSource.PIEZO_VOLTAGE)
            ui.waveformPlot.set_recording_source(1, DataRecorderSource.PIEZO_POSITION)
        await self.start_waveform_generator()
        self.plot_hysteresis()


    def calculate_hysteresis_plot_data(self) -> Tuple[List[float], List[float]]:
        """
        Calculates the data required for plotting a hysteresis curve based on recorded channel values.
        If there are enough cycles recorded, it excludes the first cycle to provide a cleaner plot.

        Returns:
            Tuple[List[float], List[float]]: A tuple containing two lists:
                - x_values: The values from channel 0, possibly excluding the first cycle if enough cycles are present.
                - y_values: The values from channel 1, possibly excluding the first cycle if enough cycles are present.
        """
        cycles = self._last_waveform_freq_hz * (self._rec_chan0.total_time_ms / 1000.0)    
        print(f"Plotting hysteresis data for {cycles} cycles...")
        if cycles >= 2:
            samples_per_cycle = int(len(self._rec_chan0.values) // cycles)
            x_values = self._rec_chan0.values[samples_per_cycle:]
            y_values = self._rec_chan1.values[samples_per_cycle:]
        else:
            x_values = self._rec_chan0.values
            y_values = self._rec_chan1.values
        return x_values, y_values


    def plot_hysteresis(self):
        """
        Plots the hysteresis curve on the UI's hysteresis plot canvas.
        This method clears the existing plot, calculates the hysteresis data (excluding the first cycle),
        and plots the data with a purple color. It then resets and autoscale the axes to fit the new data.
        Finally, it emits a status message to indicate completion.
        Returns:
            None
        """
        ui = self.ui
        plot = ui.hysteresisPlot.canvas
        ax = plot.ax1
        rec_ui = ui.waveformPlot.ui
        ax.set_xlabel(rec_ui.recsrc1ComboBox.currentData())
        ax.set_ylabel(rec_ui.recsrc2ComboBox.currentData())
        ax.set_title("Hysteresis")
        plot.clear_plot()
    

        # Drop the first cycle for a nice hysteresis plot
        x_values, y_values = self.calculate_hysteresis_plot_data()
        plot.plot_data(x_values, y_values, "Hysteresis", QColor(255, 0, 255))  # Purple color for hysteresis
        plot.update_layout()

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
        elif index == TabWidgetTabs.RESONANCE.value:
            print("Resonance tab activated")
            await self.update_resonance_voltages_ui()


    def current_waveform_type(self) -> WaveformType:
        """
        Returns the currently selected waveform type from the waveform combo box.
        """
        cb = self.ui.waveFormComboBox
        return cb.currentData(role=Qt.ItemDataRole.UserRole)   
    

    def plot_waveform(self, x_data, y_data) -> int:
        """
        Plots or updates a waveform on the UI plot canvas.

        If no lines are currently plotted, this method creates a new plot with the provided x and y data,
        labeling it as "Waveform" and using a specific color. If a line already exists, it updates the first line
        with the new data.

        Args:
            x_data (array-like): The x-axis data points for the waveform.
            y_data (array-like): The y-axis data points for the waveform.

        Returns:
            int: The number of lines present on the plot before plotting or updating.
        """
        ui = self.ui
        plot = ui.waveformPlot.canvas
        line_count = plot.get_line_count()
        if line_count == 0:
            plot.plot_data(x_data, y_data, "Waveform", QColor("#02cfff"))
        else:
            plot.update_line(0, x_data, y_data)
        return line_count


    def is_custom_waveform(self) -> bool:
        """
        Checks if the current waveform is a custom waveform.
        """
        return self.current_waveform_type() == -1
    

    def generate_waveform_from_ui(self) -> WaveformGenerator.WaveformData:
        """
        Generates a waveform using the current UI settings.

        Retrieves waveform parameters from the UI elements, including waveform type,
        low and high levels, frequency, phase shift, and duty cycle, then calls
        WaveformGenerator.generate_waveform to create the waveform data.

        Returns:
            WaveformGenerator.WaveformData: The generated waveform data object.
        """
        ui = self.ui
        if self.is_custom_waveform():
            self._custom_waveform.sample_time_ms = ui.waveSamplingPeriodSpinBox.value()
            return self._custom_waveform
        else:
            waveform = WaveformGenerator.generate_waveform(
                    waveform_type=self.current_waveform_type(),
                    low_level=ui.lowLevelSpinBox.value(),
                    high_level=ui.highLevelSpinBox.value(),
                    freq_hz=ui.freqSpinBox.value(),
                    phase_shift_rad=math.radians(ui.phaseShiftSpinBox.value()),
                    duty_cycle=ui.dutyCycleSpinBox.value() / 100.0
            )
            return waveform


    def update_waveform_plot(self):
        """
        Updates the waveform plot in the UI when the corresponding tab is active.
        """
        ui = self.ui
        if ui.tabWidget.currentIndex() != TabWidgetTabs.WAVEFORM.value:
            return
        
        print("Updating waveform plot...")
        plot = ui.waveformPlot.canvas
        waveform = self.generate_waveform_from_ui()
        line_count = self.plot_waveform(waveform.sample_times_ms, waveform.values)
        if self.is_custom_waveform():
            plot.autoscale()
        else:
            ui.waveSamplingPeriodSpinBox.setValue(waveform.sample_time_ms)
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
            waveform = self.generate_waveform_from_ui()
            self.setCursor(Qt.CursorShape.WaitCursor)
            unit = WaveformUnit.POSITION if self.ui.closedLoopCheckBox.isChecked() else WaveformUnit.VOLTAGE
            await wg.set_waveform(waveform, unit=unit, on_progress=self.report_progress)

            self.status_message.emit("Waveform uploaded successfully.", 2000)
            self.waveform_widget_change_tracker.reset()
        except Exception as e:
            self.status_message.emit(f"Error uploading waveform: {e}", 4000)
        finally:#
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.ui.mainProgressBar.reset()
            self.ui.uploadButton.setChecked(False)


    def on_upload_waveform_button_clicked(self, checked : bool):
        """
        Handles the event when the upload waveform button is clicked.
        This method is called when the user clicks the button to upload a waveform to the device.
        It retrieves the waveform data from the UI, uploads it to the device, and updates the status message accordingly.
        """
        print(f"Upload waveform button clicked: {checked}")
        if checked:
            self._waveform_task = asyncio.create_task(self.upload_waveform())
        else:
            if self._waveform_task is not None:
                self._waveform_task.cancel()
                self._waveform_task = None
            print("Waveform upload cancelled.")
            self.status_message.emit("Waveform upload cancelled.", 2000)

        
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


    async def plot_waveform_recorder_data(self) -> Tuple[DataRecorder.ChannelRecordingData, DataRecorder.ChannelRecordingData]:
        """
        Plots waveform recorder data on the UI's matplotlib canvas.

        If the 'history' checkbox is checked, previous plot lines (except the first) are faded.
        Otherwise, the waveform plot is cleared before plotting new data.
        Finally, recorder data is plotted.
        """
        ui = self.ui
        plot = ui.waveformPlot.ui.mplWidget.canvas
        if ui.waveformPlot.history_checkbox.isChecked():
            for i in range(1, plot.get_line_count()):
                self.fade_plot_line(i)
        else:
            self.clear_waveform_plot()
        return await self.plot_recorder_data(plot_widget=ui.waveformPlot.ui.mplWidget , clear_plot=False, second_axes_index=0)


    async def start_waveform_generator(self):
        """
        Asynchronously starts the waveform generator.
        """       
        ui = self.ui
        rec_ui = ui.waveformPlot.ui
        try:
            if not await self.ensure_waveform_uploaded():
                return
            
            wg = self.waveform_generator
            # If we use custom waveform, user may have modified the sampling period
            if self.is_custom_waveform():
                await wg.set_output_sampling_time(int(ui.waveSamplingPeriodSpinBox.value() * 1000))
            ui.mainProgressBar.start(5000, "start_waveform")

            recorder = await self.setup_data_recorder(
                rec_ui.recDurationSpinBox.value(), 
                ui.waveformPlot.get_recording_source(0), 
                ui.waveformPlot.get_recording_source(1))
            await recorder.set_autostart_mode(RecorderAutoStartMode.START_ON_WAVEFORM_GEN_RUN)
            await recorder.start_recording()

            ui.startWaveformButton.setEnabled(False)
            # Ensure that the right PID mode is set in case somene changed it externally
            await self.device.pid.set_mode(PidLoopMode.CLOSED_LOOP if ui.closedLoopCheckBox.isChecked() else PidLoopMode.OPEN_LOOP)
            await wg.start(cycles=self.ui.cyclesSpinBox.value())
            print("Waveform generator started successfully.")
            self.status_message.emit("Waveform generator started successfully.", 2000)
            
            self._rec_chan0 , self._rec_chan1 = await self.plot_waveform_recorder_data()

            ui.mainProgressBar.stop(success=True, context="start_waveform")
            await wg.wait_until_finished()
            self._last_waveform_freq_hz = ui.freqSpinBox.value()
            print("Total recording time: ", self._rec_chan0.total_time_ms)

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

        dev = self.device       
        self.ui.console.prompt_count += 1
        response = await dev.read_stripped_response_string(command, 10)
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
        QTimer.singleShot(0, safe_asyncslot(self.search_serial_devices))
        ui = self.ui
        ui.scrollArea.setFixedWidth(ui.scrollArea.widget().sizeHint().width() + 40)  # +40 for scroll bar width

    
    def clear_waveform_plot(self):
        """
        Clears the waveform plot in the UI.
        """
        plot = self.ui.waveformPlot.canvas
        plot.clear_plot()
        self.update_waveform_plot()


    def update_waveform_running_duration(self,):
        """
        Updates the waveform running duration in the waveform generator based on the given value.

        Args:
            value (int): The new running duration in milliseconds.
        """
        ui = self.ui
        cycles = ui.cyclesSpinBox.value()
        if self.is_custom_waveform():
            self._custom_waveform.sample_time_ms = ui.waveSamplingPeriodSpinBox.value()
            duration_ms = self._custom_waveform.cycle_time_ms * cycles
        else:
            freq_hz = ui.freqSpinBox.value()
            duration_ms = 1000 * cycles / freq_hz if freq_hz > 0 else 0.0
        ui.waveformDurationSpinBox.setValue(int(duration_ms))
        self.sync_waveform_recording_duration()


    def sync_waveform_recording_duration(self):
        """
        Synchronizes the waveform recording duration with the waveform generator's running duration.
        This method updates the recording duration spin box to match the waveform generator's calculated duration.
        """
        ui = self.ui
        if not ui.recSyncCheckBox.isChecked():
            return

        rec_ui = ui.waveformPlot.ui
        rec_ui.recDurationSpinBox.setValue(ui.waveformDurationSpinBox.value())


    async def get_resonance_spectrum(self):
        """
        Asynchronously retrieves the resonance spectrum from the device and updates the UI plot.
        """
        print("Retrieving resonance spectrum...")
        ui = self.ui
        try:
            ui.mainProgressBar.start(2000, "get_resonance_spectrum")
            self.status_message.emit("Retrieving resonance spectrum...", 0)

            analyzer = self.analyzer
            signal, sample_freq, rec_src = await analyzer.measure_impulse_response()

            plot = ui.impulsePlot.canvas
            plot.clear_plot()   
            ax = plot.ax1
            t = np.arange(len(signal)) / sample_freq  # time in seconds

            unit = await self.device.get_position_unit()
            plot.plot_data(t, signal, ax.yaxis.get_label().get_text(), QColor(0, 255, 0))

            xf, yf, res_freq = ResonanceAnalyzer.compute_resonance_spectrum(signal, sample_freq)

            plot = ui.resonancePlot.canvas
            plot.clear_plot()
            ax = plot.ax1
            ax.plot(xf, yf, color='r', label='Frequency Spectrum')
            # Set axis labels with units
            ax.set_xlim(10, 4000)
            ax.axvline(float(res_freq), color='orange', linestyle='--', label=f'Resonance: {float(res_freq):.1f} Hz')

            ax.legend(
                facecolor='darkgray', 
                edgecolor='darkgray', 
                frameon=True, 
                loc='best', 
                fontsize=10
            )

            plot.update_layout()
 

            self.status_message.emit("Resonance spectrum retrieved successfully.", 2000)
            ui.mainProgressBar.stop(success=True, context="get_resonance_spectrum")
        except Exception as e:
            print(f"Error retrieving resonance spectrum: {e}")
            self.status_message.emit(f"Error retrieving resonance spectrum: {e}", 4000)
            ui.mainProgressBar.reset()

    async def restore_previous_settings(self):
        """
        evert to the parameter values before your most recent change.
        """
        print("Restoring previous settings...")
        tracker = self.settings_widget_change_tracker
        tracker.restore_backup("previous")


    async def restore_initial_settings(self):
        """
        Load the parameters as they were when the device was first connected this session.
        """
        print("Restoring initial settings...")
        tracker = self.settings_widget_change_tracker
        tracker.restore_backup("initial")


    async def restore_default_settings(self):
        """
        Restores the default settings of the device.
        This method is called to reset the device settings to their factory defaults saved
        on first connection.
        """
        try:
            backup_path = await self.actuator_backup_filepath()
            print(f"Backup path: {backup_path}")
            if not backup_path.exists():
                print("Backup already exists. Skipping backup.")
                raise FileNotFoundError(f"Backup file not found: {backup_path}")
            await self.load_controller_param_file(str(backup_path))
        except Exception as e:
            self.status_message.emit(f"Error restoring default settings: {e}", 2000)


    async def export_controller_param(self):
        """
        Asynchronously exports controller parameters to a file.
        Iterates through controller parameter widgets, retrieves their values using either a custom
        export function or a change tracker, and converts boolean values to integers. The parameters
        are then saved to a file selected by the user via a file dialog. If an error occurs during
        file writing, a status message is emitted.
        """
        params : dict[str, str] = {}
        for cmd, widget in self._controller_param_widgets.items():
            if hasattr(widget, "export_func") and callable(widget.export_func):
                result = widget.export_func()
            else:
                result = self.settings_widget_change_tracker.get_value_of_widget(widget)

            if isinstance(result, bool):
                result = int(result)
            params[cmd] = str(result)
        
        path = (await self.actuator_backup_filepath()).parent
        filename, _ = QFileDialog.getSaveFileName(
            self.parent(),
            "Export Controller Parameters",
            str(path),
            "Device Parameter Files (*.ini)"
        )
        if not filename:
            return
        
        try:
            file = DeviceParamFile(params)
            file.write(Path(filename))
        except Exception as e:
            status_message = f"Error exporting controller parameters: {e}"
            self.status_message.emit(status_message, 4000)


    async def load_controller_param_file(self, filename: str):  
        """
        Loads controller parameters from a specified file.
        Reads the parameters from the file and updates the corresponding widgets in the UI with the loaded values.
        If an error occurs during file reading, a status message is emitted.
        """
        try:
            file = DeviceParamFile.read(Path(filename))
            for cmd, value in file.parameters.items():
                if cmd in self._controller_param_widgets:
                    print(f"Loading {cmd}: {value}")
                    widget = self._controller_param_widgets[cmd]
                    if hasattr(widget, "restore_func") and callable(widget.restore_func):
                        widget.restore_func(value)
                    else:
                        self.settings_widget_change_tracker.set_value_of_widget(widget, value)
                else:
                    print(f"Unknown command: {cmd}")
        except Exception as e:
            status_message = f"Error loading controller parameters: {e}"
            self.status_message.emit(status_message, 4000)  
    
    
    async def load_controller_param(self):
        """
        Asynchronously loads controller parameters from a file.
        Opens a file dialog to select a parameter file, reads the parameters from the file,
        and updates the corresponding widgets in the UI with the loaded values.
        If an error occurs during file reading, a status message is emitted.
        """
        path = (await self.actuator_backup_filepath()).parent
        filename, _ = QFileDialog.getOpenFileName(
            self.parent(),
            "Load Controller Parameters",
            str(path),
            "Device Parameter Files (*.ini)"
        )
        if not filename:
            return
        
        await self.load_controller_param_file(filename)


    def browse_device_param_backups(self):
        """
        Opens a file dialog to browse device parameter backups.
        The dialog allows the user to select a backup file, which is then loaded into the device.
        """
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.actuator_backup_path()))


    def read_percentage_column_with_limit(self, file_path: str, max_values: int = 1024) -> List[float]:
        """
        Reads a single-column CSV or Excel file containing percentage values (0-100).

        If the number of values exceeds max_values, asks the user whether to truncate
        or resample the data to fit the max_values limit.

        Args:
            parent (QWidget): Parent widget for dialogs.
            file_path (str): Path to CSV or Excel file.
            max_values (int): Maximum allowed number of values (default 1024).

        Returns:
            List[float]: List of percentage values as floats.

        Raises:
            ValueError: For invalid data or unsupported file types.
        """
        # Load data
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type. Provide a .csv or Excel (.xls/.xlsx) file.")

        if df.shape[1] != 1:
            raise ValueError(f"Expected exactly one column, found {df.shape[1]} columns.")

        col = df.iloc[:, 0]
        col_numeric = pd.to_numeric(col, errors='coerce')

        if col_numeric.isnull().any():
            raise ValueError("Column contains non-numeric or invalid values.")

        if not ((col_numeric >= 0) & (col_numeric <= 100)).all():
            raise ValueError("Waveform values are given in percent and must be in the range 0 to 100 inclusive.")

        values = col_numeric.tolist()

        # Check length limit
        if len(values) > max_values:
            # Ask user what to do
            msg = QMessageBox(self)
            msg.setWindowTitle("Too many values")
            msg.setText(f"The data has {len(values)} values, which exceeds the limit of {max_values}.")
            msg.setInformativeText("Do you want to truncate the data or resample it?")
            truncate_button = msg.addButton("Truncate", QMessageBox.ButtonRole.AcceptRole)
            resample_button = msg.addButton("Resample", QMessageBox.ButtonRole.AcceptRole)
            cancel_button = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
            msg.setDefaultButton(truncate_button)
            msg.exec()

            clicked = msg.clickedButton()

            if clicked == cancel_button:
                raise ValueError("User cancelled operation due to too many values.")

            elif clicked == truncate_button:
                # Truncate list
                values = values[:max_values]

            elif clicked == resample_button:
                # Resample by skipping values to reduce to max_values
                factor = (len(values) + max_values - 1) // max_values  # ceiling division
                values = values[::factor]

                # Ensure result not longer than max_values (edge case)
                values = values[:max_values]

        return values
    

    def import_custom_waveform(self):
        """
        Opens a file dialog for the user to select a waveform file (CSV or Excel),
        reads the percentage column with a limit from the selected file, and updates
        the waveform plot with the imported data.

        The default file type is Excel (*.xlsx). The imported data is stored in
        self._custom_waveform.
        """
        home_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)
        file_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Import Waveform File",
            home_dir,
            "CSV and Excel Files (*.csv *.xlsx);;CSV Files (*.csv);;Excel Files (*.xlsx)",
            "CSV and Excel Files (*.csv *.xlsx)"  # default
        )
        ui = self.ui
        self._custom_waveform = WaveformGenerator.WaveformData(self.read_percentage_column_with_limit(file_path), ui.waveSamplingPeriodSpinBox.value())
        self.update_waveform_plot()
        self.update_waveform_running_duration()