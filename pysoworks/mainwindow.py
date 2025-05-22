# This Python file uses the following encoding: utf-8
import sys
import asyncio
import logging
import os

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QDir, QCoreApplication, QSize, QObject
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
from nv200widget import NV200Widget


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_mainwindow import Ui_MainWindow


def get_icon(icon_name: str, size: int = 24, fill: bool = True) -> MaterialIcon:
    icon = MaterialIcon(icon_name, size=size, fill=fill)
    icon.set_color(QColor.fromString(os.environ.get("QTMATERIAL_PRIMARYCOLOR", "")))
    return icon



class MainWindow(QMainWindow):
    """
    Main application window for the PySoWorks UI, providing asynchronous device discovery, connection, and control features.
    Attributes:
        _device (DeviceClient): The currently connected device client, or None if not connected.
        _recorder (DataRecorder): The data recorder associated with the connected device, or None if not initialized
    """

    _device: DeviceClient = None
    _recorder : DataRecorder = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.setWindowTitle("PySoWorks")
        ui = self.ui
        ui.setupUi(self)
        nv200widget = NV200Widget(self)
        nv200widget.status_message.connect(self.statusBar().showMessage)
        self.setCentralWidget(nv200widget)

   
def setup_logging():
    """
    Configures the logging settings for the application.
    """
    logging.basicConfig(
        level=logging.WARN,
        format='%(asctime)s.%(msecs)03d | %(levelname)-6s | %(name)-25s | %(message)s',
        datefmt='%H:%M:%S'
    )     

    logging.getLogger("nv200.device_discovery").setLevel(logging.DEBUG)
    logging.getLogger("nv200.transport_protocols").setLevel(logging.DEBUG)         


if __name__ == "__main__":
    setup_logging()
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    app_path = Path(__file__).resolve().parent
    app.setWindowIcon(QIcon(str(app_path) + '/app_icon.ico'))
    apply_stylesheet(app, theme='dark_teal.xml')
    widget = MainWindow()
    widget.show()
    #sys.exit(app.exec())
    with qtinter.using_asyncio_from_qt():
        app.exec()
