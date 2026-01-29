import asyncio
from typing import Type
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QMenu, QApplication
from PySide6.QtGui import QAction
from pisoworks.ui_device_search_widget import Ui_DeviceSearchWidget
from pisoworks.ui_helpers import get_icon, get_icon_for_menu, safe_asyncslot

from nv200.device_base import PiezoDeviceBase
from nv200.device_discovery import discover_devices, DiscoverFlags, DetectedDevice
from nv200.connection_utils import connect_to_detected_device

class DeviceSearchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DeviceSearchWidget()
        self.ui.setupUi(self)
        self._device_class = None
        self._devices: list[DetectedDevice] = []

        self._current_device: PiezoDeviceBase = None
        self._search_start_cb: callable = None
        self._search_complete_cb: callable = None
        self._connect_cb: callable = None
        self._disconnect_cb: callable = None

        self._init_search_ui()

    def set_device_class(self, device_class: Type[PiezoDeviceBase]) -> None:
        self._device_class = device_class

        if self._device_class is not None:
            QTimer.singleShot(0, safe_asyncslot(self._search_serial_devices))

    def get_devices(self) -> list[DetectedDevice]:
        return self._devices

    def set_on_search_start_callback(self, callback):
        self._search_start_cb = callback

    def set_on_search_complete_callback(self, callback):
        self._search_complete_cb = callback

    def set_on_connect_callback(self, callback):
        self._connect_cb = callback

    def set_on_disconnect_callback(self, callback):
        self._disconnect_cb = callback

    def _init_search_ui(self):
        """
        Initializes the device search UI components, including buttons and combo boxes for device selection.
        """
        ui = self.ui
        ui.searchDevicesButton.setIcon(get_icon("search", size=24, fill=True))
        ui.searchDevicesButton.clicked.connect(safe_asyncslot(self._search_all_devices))

        # Create the menu
        menu = QMenu(self)

        # Create actions
        serial_action = QAction("USB Devices", ui.searchDevicesButton)
        serial_action.setIcon(get_icon_for_menu("usb"))
        ethernet_action = QAction("Ethernet Devices", ui.searchDevicesButton)
        ethernet_action.setIcon(get_icon("lan"))

        # Connect actions to appropriate slots
        serial_action.triggered.connect(safe_asyncslot(self._search_serial_devices))
        ethernet_action.triggered.connect(safe_asyncslot(self._search_ethernet_devices))

        # Add actions to menu
        menu.addAction(serial_action)
        menu.addAction(ethernet_action)

        # Set the menu to the button
        ui.searchDevicesButton.setMenu(menu)

        ui.devicesComboBox.currentIndexChanged.connect(self._on_device_selected)
        ui.connectionButton.setEnabled(False)
        ui.connectionButton.setIcon(get_icon("power", size=24, fill=True))
        ui.connectionButton.clicked.connect(safe_asyncslot(self._on_connection_button_clicked))

    def _on_device_selected(self, index: int):
        device = self.ui.devicesComboBox.itemData(index)
        self.ui.connectionButton.setEnabled(device is not None)

    async def _on_connection_button_clicked(self):
        if self._current_device:
            await self._disconnect_device()
            return

        device = self.ui.devicesComboBox.currentData()

        if not device:
            return
        
        await self._connect_device(device)

    async def _search_all_devices(self) -> None:
        """
        Initiates a search for all available devices.
        """
        await self._search_devices(self._device_class, DiscoverFlags.ALL)

    async def _search_serial_devices(self) -> None:
        """
        Initiates a search for serial devices.
        """
        await self._search_devices(self._device_class, DiscoverFlags.DETECT_SERIAL)

    async def _search_ethernet_devices(self) -> None:
        """
        Initiates a search for ethernet devices.
        """
        await self._search_devices(self._device_class, DiscoverFlags.DETECT_ETHERNET)

    async def _search_devices(self, device: Type[PiezoDeviceBase], discover_flags: DiscoverFlags) -> None:
        """
        Asynchronously searches for available devices and updates the UI accordingly.
        """
        ui = self.ui
        ui.searchDevicesButton.setEnabled(False)
        ui.connectionButton.setEnabled(False)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        error = None
        
        if self._search_start_cb:
            await self._search_start_cb()
       
        try:
            self._devices = []
            self._devices = await discover_devices(flags=discover_flags, device_class=device)    
        except Exception as e:
            error = e
        finally:
            QApplication.restoreOverrideCursor()
            self.ui.searchDevicesButton.setEnabled(True)
            self.ui.devicesComboBox.clear()
            
            if self._devices:
                for device in self._devices:
                    self.ui.devicesComboBox.addItem(f"{device}", device)
            else:
                self.ui.devicesComboBox.addItem("No devices found.", None)
            
            if self._search_complete_cb:
                await self._search_complete_cb(self._devices, error)

    async def _disconnect_device(self) -> None:
        """
        Disconnects from the currently connected device and updates the UI.
        """
        self.ui.connectionButton.setEnabled(False)
        
        if self._current_device:
            await self._current_device.close()
        
        if self._disconnect_cb:
            await self._disconnect_cb()

        self._current_device = None
        
        self.ui.connectionButton.setText("Connect")
        self.ui.connectionButton.setEnabled(True)

    async def _connect_device(self, device: DetectedDevice) -> None:
        """
        Asynchronously connects to the selected device.
        """
        self.setCursor(Qt.CursorShape.WaitCursor)
        error = None

        try:
            await self._disconnect_device()

            self.ui.connectionButton.setEnabled(False)
            self._current_device = await connect_to_detected_device(device)
            self.ui.connectionButton.setText("Disconnect")
        except Exception as e:
            self.ui.connectionButton.setText("Connect")
            error = e
        finally:
            try:
                if self._connect_cb:
                    await self._connect_cb(self._current_device, error)
            except Exception:
                self.ui.connectionButton.setText("Connect")

            self.ui.connectionButton.setEnabled(True)
            self.setCursor(Qt.CursorShape.ArrowCursor)
