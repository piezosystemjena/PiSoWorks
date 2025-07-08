# This Python file uses the following encoding: utf-8
import sys
import asyncio
import logging
import os

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette
import qtinter
from matplotlib.backends.backend_qtagg import FigureCanvas
from qt_material_icons import MaterialIcon

from nv200.shared_types import DetectedDevice, DiscoverFlags
from nv200.device_discovery import discover_devices
from nv200.spibox_device import SpiBoxDevice
from nv200.connection_utils import connect_to_detected_device


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from pysoworks.ui_spiboxwidget import Ui_SpiBoxWidget


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
        self.ui = Ui_SpiBoxWidget()
        ui = self.ui
        ui.setupUi(self)
        ui.searchDevicesButton.clicked.connect(qtinter.asyncslot(self.search_devices))
        ui.devicesComboBox.currentIndexChanged.connect(self.on_device_selected)
        ui.connectButton.clicked.connect(qtinter.asyncslot(self.connect_to_device))
        ui.moveProgressBar.set_duration(5000)
        ui.moveProgressBar.set_update_interval(20)
        ui.singleDatasetGroupBox.setEnabled(False)
        ui.sendSingleButton.clicked.connect(qtinter.asyncslot(self.send_single_dataset))


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
        ui.moveProgressBar.start(5000, "search_devices")
        try:
            print("Discovering devices...")
            devices = await discover_devices(flags=DiscoverFlags.ALL | DiscoverFlags.ADJUST_COMM_PARAMS, device_class=SpiBoxDevice)    
            
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