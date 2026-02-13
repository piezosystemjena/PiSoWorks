# This Python file uses the following encoding: utf-8
from typing import List
import sys
import asyncio
import logging
import os
import math
import numpy

from PySide6.QtWidgets import QApplication, QWidget, QMenu, QSizePolicy
from PySide6.QtCore import Qt, Signal, QTimer, QEvent
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

        # Handle tab switching and content size changes
        self.ui.channelTabWidget.currentChanged.connect(self.updateTabSize)
        self.ui.channel1Tab.installEventFilter(self)
        self.ui.channel2Tab.installEventFilter(self)
        self.ui.channel3Tab.installEventFilter(self)
        
        # Set initial tab size for the first tab
        QTimer.singleShot(0, lambda: self.updateTabSize(self.ui.channelTabWidget.currentIndex()))

        # Initialize waveform plot
        self.ui.waveformPlot.show_export_action()

        # Do not show dirty tracking for the waveform option widgets
        self.ui.waveformOptions1.set_show_dirty_indicators(False)
        self.ui.waveformOptions2.set_show_dirty_indicators(False)
        self.ui.waveformOptions3.set_show_dirty_indicators(False)

        # Plot timer, to delay plotting after option changes
        self._plot_timer = QTimer(self)
        self._plot_timer.setSingleShot(True)
        self._plot_timer.timeout.connect(self.plot_all_waveforms)

        self._custom_waveform = WaveformGenerator.WaveformData() # Placeholder for custom waveform

        style_manager.style.dark_mode_changed.connect(self.set_dark_mode)
        style_manager.style.stylesheet_changed.connect(self.schedule_left_nav_relayout)
        self.schedule_left_nav_relayout()


    def updateTabSize(self, index=None):
        """
        Adjusts the tab widget height to match the currently selected tab's content.
        """
        try:
            if index is None:
                index = self.ui.channelTabWidget.currentIndex()
            
            # Set size policies: Ignored for hidden tabs, Preferred for visible tab
            for i in range(self.ui.channelTabWidget.count()):
                policy = QSizePolicy.Policy.Preferred if i == index else QSizePolicy.Policy.Ignored
                self.ui.channelTabWidget.widget(i).setSizePolicy(policy, policy)
            
            # Calculate and set the tab widget height
            current_widget = self.ui.channelTabWidget.widget(index)
            tab_bar_height = self.ui.channelTabWidget.tabBar().height()
            total_height = current_widget.sizeHint().height() + tab_bar_height
            
            self.ui.channelTabWidget.setMaximumHeight(total_height)
            self.ui.channelTabWidget.updateGeometry()
        except Exception as e:
            # Log error but do not crash, this might happen because the tab was already destroyed
            print(f"Error updating tab size: {e}")


    def eventFilter(self, obj, event):
        """
        Detects when tab content size changes and updates tab widget height accordingly.
        """
        if event.type() == QEvent.Type.LayoutRequest:
            if obj == self.ui.channelTabWidget.currentWidget():
                QTimer.singleShot(0, self.updateTabSize)
        return super().eventFilter(obj, event)   


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


    def set_dark_mode(self, dark: bool):
        """
        Handler after the dark mode has changed.

        Args:
            dark (bool): The new dark mode state.
        """
        self.ui.waveformPlot.set_dark_mode(dark)
        self.plot_all_waveforms()


    def schedule_left_nav_relayout(self):
        """
        Schedules a relayout so the left navigation column resizes after font changes.
        """
        QTimer.singleShot(0, self.update_left_nav_layout)
        QTimer.singleShot(100, self.update_left_nav_layout)


    def update_left_nav_layout(self):
        """
        Forces layout updates for the left navigation column so it reflects font size changes.
        """
        ui = self.ui
        if ui is None:
            return

        left_widgets = [ui.singleDatasetGroupBox, ui.multipleDatasetGroupBox]
        for widget in left_widgets:
            widget.ensurePolished()
            widget.updateGeometry()
            widget.adjustSize()

        min_width = max(widget.sizeHint().width() for widget in left_widgets)
        min_width = max(0, min_width + 8)

        for widget in left_widgets:
            widget.setSizePolicy(QSizePolicy.Policy.Fixed, widget.sizePolicy().verticalPolicy())
            widget.setFixedWidth(min_width)

        ui.channelTabWidget.updateGeometry()
        ui.channelTabWidget.adjustSize()

        ui.verticalLayout_2.invalidate()
        ui.horizontalLayout_2.invalidate()
        ui.verticalLayout_3.invalidate()
        self.updateGeometry()
        self.adjustSize()
        self.update()


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
        ui = self.ui
        ui.deviceSearchWidget.set_device_class(SpiBoxDevice)
        ui.deviceSearchWidget.set_on_search_start_callback(self.handle_search_devices_start)
        ui.deviceSearchWidget.set_on_search_complete_callback(self.handle_search_devices_end)
        ui.deviceSearchWidget.set_on_connect_callback(self.handle_connect_device)
        ui.deviceSearchWidget.set_on_disconnect_callback(self.handle_disconnect_device)

    
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
        self.ui.waveformOptions1.set_sampling_period_step(0.05)
        self.ui.waveformOptions2.set_sampling_period_step(0.05)
        self.ui.waveformOptions3.set_sampling_period_step(0.05)

        self.ui.waveformPlot.canvas.clear_plot()
        self.ui.waveformPlot.canvas.get_axes(0).set_ylabel('Piezo Position (%)')

        # If connected to a device, show waveform preview and get current waveform status
        if connected:
            self._plot_timer.start(100)
            asyncio.create_task(self.reflect_waveform_status())

    
    async def handle_search_devices_start(self):
        """
        Handles the start of the device search process by updating the UI status and progress bar.
        """
        self.status_message.emit("Searching for devices...", 0)
        self.ui.moveProgressBar.start(3000)

    
    async def handle_search_devices_end(self, devices: List[DetectedDevice], error: Exception | None):
        """
        Handles the end of the device search process by updating the UI status and progress bar.
        """
        if devices:
            self.ui.moveProgressBar.stop(success=True, context="search_devices")
        else:
            self.ui.moveProgressBar.reset()

        self.status_message.emit("", 0)
        

    async def handle_connect_device(self, device: SpiBoxDevice, error: Exception | None):
        """
        Handles the event when the DeviceSearchWidget connects to a device.
        """
        if error:
            self.reset_ui(False)
            self.status_message.emit(f"Connection failed: {error}", 2000)
            return
        
        self._device = device
        self.reset_ui(True)
        print(f"Connected to {device.device_info}.")


    async def handle_disconnect_device(self):
        """
        Handles the event when the DeviceSearchWidget disconnects from a device.
        """
        self.reset_ui(False)

        # Cancel any ongoing waveform task
        if self._waveform_task is not None:
            self._waveform_task.cancel()

    
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
        self.updateTabSize(self.ui.channelTabWidget.currentIndex())

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
        # Do not plot if no waveform data is available
        if waveform is None or len(waveform.values) == 0:
            return

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
        if len(original_list) == 0:
            return []
        
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
        # Check if custom waveform
        if option.get_waveform_type() == -1:
            data = option.get_custom_waveform_data()

            # Do not generate if no data is provided
            if data is None or len(data) == 0:
                return None

            self._custom_waveform = WaveformGenerator.WaveformData(
                data,
                option.get_sampling_period()
            )
            return self._custom_waveform
        
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
        self.ui.deviceSearchWidget.cleanup()