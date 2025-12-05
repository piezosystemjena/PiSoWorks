# This Python file uses the following encoding: utf-8
import sys
import asyncio
import logging
import os
import math
import numpy

from PySide6.QtWidgets import QApplication, QWidget, QMenu
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPalette, QIcon, QAction, QColor
import qtinter
from matplotlib.backends.backend_qtagg import FigureCanvas
from qt_material_icons import MaterialIcon

from nv200.shared_types import DetectedDevice, DiscoverFlags
from nv200.device_discovery import discover_devices
from nv200.spibox_device import SpiBoxDevice
from nv200.connection_utils import connect_to_detected_device
from pisoworks.style_manager import style_manager
from pisoworks.ui_helpers import get_icon, get_icon_for_menu, set_combobox_index_by_value, safe_asyncslot
from nv200.waveform_generator import WaveformGenerator, WaveformType, WaveformUnit

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from pisoworks.ui_spiboxwidget import Ui_SpiBoxWidget




class SpiBoxWidget(QWidget):
    """
    Main application window for the PiSoWorks UI, providing asynchronous device discovery, connection, and control features.
    Attributes:
        _device (DeviceClient): The currently connected device client, or None if not connected.
        _recorder (DataRecorder): The data recorder associated with the connected device, or None if not initialized
    """

    _device: SpiBoxDevice = None
    status_message = Signal(str, int)  # message text, timeout in ms

    def __init__(self, parent=None):
        super().__init__(parent)

        self._discover_flags : DiscoverFlags = DiscoverFlags.ALL
        self.ui = Ui_SpiBoxWidget()
        self._waveform_task = None
        self._initialized = False

        ui = self.ui
        ui.setupUi(self)
        self.init_device_search_ui()
        self.reset_ui(False)

        # Create a waveform generator without any device attached - this will only generate the waveform data
        # The data can then be sent using the SpiBoxDevice class
        self.waveform_generator = WaveformGenerator(None)
        self.waveform_response = []

        # Initialize Button and Checkbox event listeners
        ui.sendSingleButton.clicked.connect(qtinter.asyncslot(self.send_single_dataset))
        ui.startWaveformButton.clicked.connect(self.on_start_waveform)
        ui.infiniteCyclesCheckBox.toggled.connect(self.on_infinite_cycles_checked)
        ui.channelTabWidget.currentChanged.connect(self.on_channel_switched)
        ui.getResponseButton.clicked.connect(self.on_get_waveform_response)

        # Initialize option changed event listeners
        self.ui.waveformOptions1.optionChanged.connect(self.on_option_changed)
        self.ui.waveformOptions2.optionChanged.connect(self.on_option_changed)
        self.ui.waveformOptions3.optionChanged.connect(self.on_option_changed)
        self.ui.cyclesSpinBox.valueChanged.connect(self.on_option_changed)
        self.ui.infiniteCyclesCheckBox.toggled.connect(self.on_option_changed)
        self.ui.enabledCheckbox1.toggled.connect(self.on_enabled_changed)
        self.ui.enabledCheckbox2.toggled.connect(self.on_enabled_changed)
        self.ui.enabledCheckbox3.toggled.connect(self.on_enabled_changed)

        # Initialize waveform plot
        self.ui.waveformPlot.show_export_action()

        # Do not show dirty tracking for the waveform option widgets
        self.ui.waveformOptions1.set_show_dirty_indicators(False)
        self.ui.waveformOptions2.set_show_dirty_indicators(False)
        self.ui.waveformOptions3.set_show_dirty_indicators(False)

        self._plot_timer = QTimer(self)
        self._plot_timer.setSingleShot(True)
        self._plot_timer.timeout.connect(self.plot_all_waveforms)

        style_manager.style.dark_mode_changed.connect(self.set_dark_mode)


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


    def set_dark_mode(self, dark: bool):
        """
        Handler after the dark mode has changed.

        Args:
            dark (bool): The new dark mode state.
        """
        self.ui.waveformPlot.set_dark_mode(dark)
        self.plot_all_waveforms()


    def on_infinite_cycles_checked(self, value):
        """
        Handles the event when the infinite cycles checkbox is toggled.
        Updates the visibility of the cycles selection controls based on the checkbox state.
        """
        self.show_cycles_selection(not value)


    def show_cycles_selection(self, value):
        """
        Shows or hides the cycles selection UI elements.
        Controls the visibility of the cycles label and spin box based on the provided value.
        """
        self.ui.cyclesLabel.setVisible(value)
        self.ui.cyclesSpinBox.setVisible(value)

    
    def update_target_pos_edits(self):
        """
        Updates the target position edit controls for all three channels.
        Sets the setpoint options to use percentage units with a range of 0-100% for each channel.
        """
        self.ui.waveformOptions1.set_setpoint_options("%", [0, 100])
        self.ui.waveformOptions2.set_setpoint_options("%", [0, 100])
        self.ui.waveformOptions3.set_setpoint_options("%", [0, 100])


    def set_groupbox_enabled(self, value):
        """
        Enables or disables the single dataset and multiple dataset group boxes.
        Used to control UI availability based on device connection status.
        """
        self.ui.singleDatasetGroupBox.setEnabled(value)
        self.ui.multipleDatasetGroupBox.setEnabled(value)


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
                                       
        ui.connectButton.clicked.connect(qtinter.asyncslot(self.connect_to_device))
        ui.connectButton.setIcon(get_icon("power", size=24, fill=True))
        ui.searchDevicesButton.clicked.connect(qtinter.asyncslot(self.search_devices))
        ui.devicesComboBox.currentIndexChanged.connect(self.on_device_selected)


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
        self.set_groupbox_enabled(False)
        self.status_message.emit("Searching for devices...", 0)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        if self._device is not None:
            await self._device.close()
            self._device = None
        
        print("Searching...")
        ui.moveProgressBar.start(300)
        try:
            print("Discovering devices...")
            devices = await discover_devices(flags=self._discover_flags | DiscoverFlags.ADJUST_COMM_PARAMS, device_class=SpiBoxDevice)    
            
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

    
    def selected_device(self) -> DetectedDevice:
        """
        Returns the currently selected device from the devicesComboBox.
        """
        index = self.ui.devicesComboBox.currentIndex()
        if index == -1:
            return None
        return self.ui.devicesComboBox.itemData(index, role=Qt.UserRole)
    
    
    async def disconnect_from_device(self, update_ui = True):
        """
        Asynchronously disconnects from the currently connected device.
        """
        if self._device is None:
            print("No device connected.")
            return

        await self._device.close()
        self._device = None     
          
        if update_ui:
            self.reset_ui(False)

        # Cancel any ongoing waveform task
        if self._waveform_task is not None:
            self._waveform_task.cancel()

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
            self.status_message.emit(f"Connected to {detected_device.identifier}.", 2000)
            print(f"Connected to {detected_device.identifier}.")
        except Exception as e:
            self.status_message.emit(f"Connection failed: {e}", 2000)
            print(f"Connection failed: {e}")
            return
        finally:
            self.reset_ui(True)
    

    def reset_ui(self, connected):
        """
        Resets the UI elements to their initial state.
        """
        self.set_groupbox_enabled(connected)
        self.setCursor(Qt.ArrowCursor)
        self.set_waveform_ui_state(SpiBoxDevice.WaveformState.STOPPED)
        self.update_target_pos_edits()

        # Set waveform option widgets to dirty state
        self.ui.waveformOptions1.set_dirty()
        self.ui.waveformOptions2.set_dirty()
        self.ui.waveformOptions3.set_dirty()

        # Sampling period is fixed to 50us for NV200 in SPI mode
        self.ui.waveformOptions1.set_sampling_period_readonly(True)
        self.ui.waveformOptions2.set_sampling_period_readonly(True)
        self.ui.waveformOptions3.set_sampling_period_readonly(True)

        self.ui.waveformPlot.canvas.clear_plot()
        self.ui.waveformPlot.canvas.get_axes(0).set_ylabel('Piezo Position (%)')

        # If connected to a device, show waveform preview and get current waveform status
        if connected:
            self._plot_timer.start(100)
            asyncio.create_task(self.reflect_waveform_status())

    
    async def reflect_waveform_status(self):
        """
        Fetches the current waveform status from the device and updates the UI accordingly.
        """
        if self._device is None:
            return
        
        try:
            wf_state = await self._device.get_waveform_status()
            self.set_waveform_ui_state(wf_state)
        except Exception as e:
            self.status_message.emit(f" Error fetching waveform status: {e}", 4000)

        return wf_state


    async def send_single_dataset(self):
        """
        Handles the event when the send single button is clicked.
        Sends a single dataset to the connected SPI Box device and updates the UI with the response.
        """
        if self._device is None:
            self.status_message.emit("No device connected.", 2000)
            return
        
        try:
            rxdata = await self._device.set_setpoints_percent(
                self.ui.singleDatasetSendCh1SpinBox.value(),
                self.ui.singleDatasetSendCh2SpinBox.value(),
                self.ui.singleDatasetSendCh3SpinBox.value()
            )

            self.ui.singleDatasetReceiveCh1SpinBox.setValue(rxdata[0])
            self.ui.singleDatasetReceiveCh2SpinBox.setValue(rxdata[1])
            self.ui.singleDatasetReceiveCh3SpinBox.setValue(rxdata[2])

        except Exception as e:
            self.status_message.emit(f" Error sending dataset: {e}", 4000)
            return


    def plot_all_waveforms(self):
        """
        Plots all waveforms for the currently selected channel.
        Generates the waveform data, clears the existing plot, and displays both the response and generated waveform.
        """
        # Generate waveform for the currently selected channel
        selected_channel = self.ui.channelTabWidget.currentIndex()
        generated_waveform = self.generate_waveform_for_channel(selected_channel)
        enabled = [self.ui.enabledCheckbox1, self.ui.enabledCheckbox2, self.ui.enabledCheckbox3][selected_channel].isChecked()

        # Clear existing plot and redraw response and preview waveforms
        self.clear_waveform_plot()
        self.plot_waveform(
            generated_waveform,
            self.ui.cyclesSpinBox.value() if not self.ui.infiniteCyclesCheckBox.isChecked() else 1,
            enabled
        )
        self.plot_response(self.waveform_response)


    def on_channel_switched(self):
        """
        Handles the event when the user switches to a different channel tab.
        Redraws the waveform plot to display the waveform for the newly selected channel.
        """
        if self._device is None:
            return

        self.plot_all_waveforms()


    def on_option_changed(self):
        """
        Handles the event when any waveform option is changed.
        Redraws the waveform plot to reflect the updated parameters.
        """
        if self._device is None:
            return
        
        self._plot_timer.start(100)


    def on_enabled_changed(self):
        """
        Handles the event when any channel enabled checkbox is changed.
        Redraws the waveform plot to reflect the updated enabled state and sets the dirty state.
        """
        if self._device is None:
            return
        
        self.ui.waveformOptions1.set_dirty()
        self.ui.waveformOptions2.set_dirty()
        self.ui.waveformOptions3.set_dirty()

        self.on_option_changed()

    def on_start_waveform(self):
        """
        Handles the event when the start button is clicked.
        This method is called when the user clicks the button to start a waveform output on the SPI Box.
        It retrieves the waveform data from the UI, uploads it to the device, and updates the status message accordingly.
        """
        if self._device is None:
            self.status_message.emit("No device connected.", 2000)
            return
        
        self._waveform_task = asyncio.create_task(self.handle_start_button())


    def on_get_waveform_response(self):
        """
        Handles the event when the get waveform response button is clicked.
        This method is called when the user clicks the button to fetch the waveform response from the SPI Box.
        It retrieves the response data from the device and updates the status message accordingly.
        """
        if self._device is None:
            self.status_message.emit("No device connected.", 2000)
            return

        self._waveform_task = asyncio.create_task(self.get_waveform_response())


    async def handle_start_button(self):
        status = None
        
        try:
            status = await self.reflect_waveform_status()
        except Exception as e:
            self.status_message.emit(f" Error fetching waveform status: {e}", 4000)
            return

        if status == SpiBoxDevice.WaveformState.STOPPED:
            self._waveform_task = await self.upload_waveforms()
        else:
            self._waveform_task = await self.stop_waveforms()


    async def stop_waveforms(self):
        """
        Asynchronously stops the currently running waveform output on the device.
        Changes the waveform state to stopped.
        """
        # Update UI state
        self.setCursor(Qt.CursorShape.WaitCursor)
        self.ui.startWaveformButton.setEnabled(False)

        try:
            await self._device.stop_waveforms()

        except Exception as e:
            self.status_message.emit(f" Error stopping waveforms: {e}", 4000)
            return

        self.set_waveform_ui_state(SpiBoxDevice.WaveformState.STOPPED)
        self.setCursor(Qt.CursorShape.ArrowCursor)


    async def upload_waveforms(self):
        """
        Asynchronously uploads and starts the waveform output on the device.
        """
        if self._device is None:
            self.status_message.emit(f" No device connected.", 4000)
            return

        try:
            infinite = self.ui.infiniteCyclesCheckBox.isChecked()

            # Update UI state
            self.status_message.emit(f" Generating waveforms...", 0)
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.set_waveform_ui_state(SpiBoxDevice.WaveformState.RUNNING)

            # Generate and plot waveforms
            waveforms = self.generate_waveforms_from_ui()

            self.waveform_response = []  # Clear previous response
            self.plot_all_waveforms()

            # Configure waveform
            actual_cycles = self.ui.cyclesSpinBox.value() if not self.ui.infiniteCyclesCheckBox.isChecked() else 0
            await self._device.set_waveform_cycles(actual_cycles, actual_cycles, actual_cycles)
            
            await self._device.set_waveform_sample_factors(
                waveforms[0].sample_factor if waveforms[0] is not None else 1,
                waveforms[1].sample_factor if waveforms[1] is not None else 1,
                waveforms[2].sample_factor if waveforms[2] is not None else 1
            )

            if self.any_waveform_changed():
                await self._device.upload_waveform_samples(
                    ch1 = waveforms[0].values if waveforms[0] is not None else None,
                    ch2 = waveforms[1].values if waveforms[1] is not None else None,
                    ch3 = waveforms[2].values if waveforms[2] is not None else None,
                    on_progress = lambda current, total: self.on_waveform_progress(current, total, True)
                )

                self.ui.waveformOptions1.clear_dirty()
                self.ui.waveformOptions2.clear_dirty()
                self.ui.waveformOptions3.clear_dirty()

            self.ui.moveProgressBar.reset()

            # Start waveform
            await self._device.start_waveforms()

            # Handle single vs infinite cycles
            if not infinite:
                self.status_message.emit(f" Waiting for waveform completion...", 0)
                await self._device.await_waveform_completion()

            await self.reflect_waveform_status()
            self.status_message.emit(f" Done", 2000)

        except Exception as e:
            self.status_message.emit(f" Error uploading waveforms: {e}", 4000)
            self.set_waveform_ui_state(SpiBoxDevice.WaveformState.STOPPED)
        
        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)


    async def get_waveform_response(self):
        """
        Asynchronously retrieves the waveform response data from the device.
        Updates the waveform response attribute and redraws the waveform plot.
        """
        if self._device is None:
            self.status_message.emit(f" No device connected.", 4000)
            return
        
        # Update UI state
        self.ui.startWaveformButton.setEnabled(False)
        self.ui.getResponseButton.setEnabled(False)
        self.status_message.emit(f" Fetching waveform response...", 0)

        # Fetch and plot response
        try:
            sample_count = await self._device.get_response_samples_count()

            if sample_count == 0:
                self.status_message.emit(f" No waveform response data available.", 4000)
                self.ui.startWaveformButton.setEnabled(True)
                self.ui.getResponseButton.setEnabled(True)
                return

            step = max(1, math.ceil(sample_count / 1000))  # Limit to 1000 samples for performance

            rxdata = await self._device.get_waveform_response(
                step_size = step,
                max_samples = 1000,
                on_progress = lambda current, total: self.on_waveform_progress(current, total, False)
            )
            self.waveform_response = rxdata

            self.plot_all_waveforms()
            self.status_message.emit(f" Done", 2000)

        except Exception as e:
            self.status_message.emit(f" Error fetching waveform response: {e}", 4000)
            return

        # Update UI state
        self.ui.moveProgressBar.reset()
        self.ui.startWaveformButton.setEnabled(True)
        self.ui.getResponseButton.setEnabled(True)


    def on_waveform_progress(self, current_sample, total_samples, is_upload):
        """
        Handles progress updates during waveform upload or response fetching.
        Updates the status message and progress bar based on the current sample being processed.
        """
        percentage = (current_sample / total_samples) * 100

        if current_sample % 10 != 0 and current_sample != total_samples:
            return  # Update only on every 10 increment for performance

        operation = "Uploading" if is_upload else "Fetching"
        self.ui.moveProgressBar.setMaximum(total_samples)
        self.ui.moveProgressBar.setValue(current_sample)
        self.status_message.emit(f" {operation} waveform - sample {current_sample} of {total_samples} [{percentage:.1f}%]", 0)


    def clear_waveform_plot(self):
        """
        Clears the waveform plot canvas, removing all previously drawn waveforms.
        """
        self.ui.waveformPlot.canvas.clear_plot()


    def plot_response(self, channels):
        """
        Plots the response data received from the device for all channels.
        Displays each channel's response as a colored line on the waveform plot.
        """
        if channels is None or len(channels) == 0:
            return

        for i, channel in enumerate(channels):
            self.ui.waveformPlot.canvas.add_line(
                x_data = channel.sample_times_ms,
                y_data = channel.values,
                label = f"Channel {i+1}",
                color = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255)][i]
            )


    def plot_waveform(self, waveform, cycle_count = 1, enabled = True):
        """
        Plots the generated waveform on the canvas.
        The waveform is repeated for the specified number of cycles and displayed with a dashed line if
        the channel is disabled.
        """
        line_color = QColor(200, 200, 200) if style_manager.style.is_current_theme_dark() else QColor(50, 50, 50)

        self.ui.waveformPlot.canvas.add_line(
            x_data = self.extend_sample_ms_list(waveform.sample_times_ms, cycle_count),
            y_data = numpy.tile(waveform.values, cycle_count),
            label = f"Waveform",
            color = line_color,
            linestyle = '--' if not enabled else '-'
        )
    

    def extend_sample_ms_list(self, original_list, factor):
        """
        Extends the original sample time list by the given factor.
        Each sample time is repeated 'factor' times to match the extended waveform data.
        """
        sample_time = original_list[1]
        total_samples = len(original_list) * factor

        return [i * sample_time for i in range(total_samples)]


    def generate_waveforms_from_ui(self):
        """
        Generates waveform data for all enabled channels based on the current UI settings.
        Returns a list of waveform arrays, with None for disabled channels.
        """
        waveforms = []

        # Generate a waveform for each channel
        for channel in range(3):
            waveform = None
            enabled = [self.ui.enabledCheckbox1, self.ui.enabledCheckbox2, self.ui.enabledCheckbox3][channel].isChecked()
            
            # Only generate waveform if the channel is enabled
            if enabled:
                waveform = self.generate_waveform_for_channel(channel)

            waveforms.append(waveform)

        return waveforms
    
    
    def generate_waveform_for_channel(self, channel_index):
        """
        Generates a waveform for the specified channel index (0-2).
        Returns the generated waveform object based on the channel's option settings.
        """
        if channel_index < 0 or channel_index > 2:
            return None

        option = [self.ui.waveformOptions1, self.ui.waveformOptions2, self.ui.waveformOptions3][channel_index]
        return self.generate_waveform_for_option(option)
    

    def generate_waveform_for_option(self, option):
        """
        Generates a waveform based on the provided option settings.
        Supports standard waveform types (sine, triangle, square) and placeholder for custom waveforms.
        """
        if option.get_waveform_type() == -1:
            # TODO: Custom waveform handling
            # self._custom_waveform.sample_time_ms = option.waveSamplingPeriodSpinBox.value()
            # return self._custom_waveform
            return None
        
        waveform = WaveformGenerator.generate_waveform(
            waveform_type       = option.get_waveform_type(),
            low_level           = option.get_low_level(),
            high_level          = option.get_high_level(),
            freq_hz             = option.get_frequency(),
            phase_shift_rad     = math.radians(option.get_phase_shift()),
            duty_cycle          = option.get_duty_cycle() / 100.0
        )

        option.set_sampling_period(waveform.sample_time_ms)

        return waveform
    
    
    def set_waveform_ui_state(self, state):
        """
        Handles changes in the waveform state and updates the UI accordingly.
        Updates the start/stop button text, icon, and enabled state based on whether the waveform is stopped, running, or running infinitely.
        """
        if state == SpiBoxDevice.WaveformState.STOPPED:
            self.ui.startWaveformButton.setEnabled(True)
            self.ui.getResponseButton.setEnabled(True)
            self.ui.sendSingleButton.setEnabled(True)
            self.ui.startWaveformButton.setText("Start")
            self.ui.startWaveformButton.setIcon(get_icon("play_arrow", size=24, fill=True))
            self.ui.getResponseButton.setIcon(get_icon("show_chart", size=24, fill=True))
        elif state == SpiBoxDevice.WaveformState.RUNNING:
            self.ui.startWaveformButton.setEnabled(True)
            self.ui.getResponseButton.setEnabled(False)
            self.ui.sendSingleButton.setEnabled(False)
            self.ui.startWaveformButton.setText("Stop")
            self.ui.startWaveformButton.setIcon(get_icon("stop", size=24, fill=True))
            self.ui.getResponseButton.setIcon(get_icon("show_chart", size=24, fill=True))
        elif state == SpiBoxDevice.WaveformState.RUNNING_INFINITE:
            self.ui.startWaveformButton.setEnabled(True)
            self.ui.getResponseButton.setEnabled(False)
            self.ui.sendSingleButton.setEnabled(False)
            self.ui.startWaveformButton.setText("Stop")
            self.ui.startWaveformButton.setIcon(get_icon("stop", size=24, fill=True))
            self.ui.getResponseButton.setIcon(get_icon("show_chart", size=24, fill=True))


    def any_waveform_changed(self):
        """
        Checks if any of the waveform option widgets have unsaved changes.
        Returns True if any waveform options are dirty, otherwise False.
        """
        return (self.ui.waveformOptions1.is_dirty() or
                self.ui.waveformOptions2.is_dirty() or
                self.ui.waveformOptions3.is_dirty())


    def cleanup(self):
        """
        Cleans up resources by initiating an asynchronous disconnection from the device.
        This function needs to get called, before the widget is deleted
        """
        result = asyncio.create_task(self.disconnect_from_device(update_ui = False))