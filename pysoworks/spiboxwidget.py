# This Python file uses the following encoding: utf-8
import sys
import asyncio
import logging
import os

from PySide6.QtWidgets import QApplication, QWidget, QMenu
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette, QIcon, QAction
import qtinter
from matplotlib.backends.backend_qtagg import FigureCanvas
from qt_material_icons import MaterialIcon

from nv200.shared_types import DetectedDevice, DiscoverFlags
from nv200.device_discovery import discover_devices
from nv200.spibox_device import SpiBoxDevice
from nv200.connection_utils import connect_to_detected_device
from pysoworks.style_manager import StyleManager, style_manager
from pysoworks.ui_helpers import get_icon, get_icon_for_menu, set_combobox_index_by_value, safe_asyncslot

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from pysoworks.ui_spiboxwidget import Ui_SpiBoxWidget




class SpiBoxWidget(QWidget):
    """
    Main application window for the PySoWorks UI, providing asynchronous device discovery, connection, and control features.
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
        ui = self.ui
        ui.setupUi(self)
        self.init_device_search_ui()
        ui.singleDatasetGroupBox.setEnabled(False)
        ui.sendSingleButton.clicked.connect(qtinter.asyncslot(self.send_single_dataset))
        style_manager.style.dark_mode_changed.connect(ui.waveformPlot.set_dark_mode)


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
        ui.singleDatasetGroupBox.setEnabled(False)
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
    
    
    async def disconnect_from_device(self):
        """
        Asynchronously disconnects from the currently connected device.
        """
        if self._device is None:
            print("No device connected.")
            return

        await self._device.close()
        self._device = None       
            


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
            self.ui.singleDatasetGroupBox.setEnabled(True)
            self.status_message.emit(f"Connected to {detected_device.identifier}.", 2000)
            print(f"Connected to {detected_device.identifier}.")
        except Exception as e:
            self.status_message.emit(f"Connection failed: {e}", 2000)
            print(f"Connection failed: {e}")
            return
        finally:
            self.setCursor(Qt.ArrowCursor)


    async def send_single_dataset(self):
        """
        Handles the event when the send single button is clicked.
        Sends a single dataset to the connected SPI Box device and updates the UI with the response.
        """
        rxdata = await self._device.set_setpoints_percent(
            self.ui.singleDatasetSendCh1SpinBox.value(),
            self.ui.singleDatasetSendCh2SpinBox.value(),
            self.ui.singleDatasetSendCh3SpinBox.value()
        )

        self.ui.singleDatasetReceiveCh1SpinBox.setValue(rxdata[0])
        self.ui.singleDatasetReceiveCh2SpinBox.setValue(rxdata[1])
        self.ui.singleDatasetReceiveCh3SpinBox.setValue(rxdata[2])

    def cleanup(self):
        """
        Cleans up resources by initiating an asynchronous disconnection from the device.
        This function needs to get called, before the widget is deleted
        """
        result = asyncio.create_task(self.disconnect_from_device())