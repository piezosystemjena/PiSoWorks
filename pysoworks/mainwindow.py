# This Python file uses the following encoding: utf-8
import sys
import asyncio
import logging
import os

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QDir, QCoreApplication, QSize, QObject
from PySide6.QtGui import QColor, QIcon, QPalette
from PySide6.QtWidgets import QDoubleSpinBox
import qtinter
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from nv200.shared_types import DetectedDevice, PidLoopMode, DiscoverFlags
from nv200.device_discovery import discover_devices
from nv200.device_interface import DeviceClient, create_device_client
from nv200.data_recorder import DataRecorder, DataRecorderSource, RecorderAutoStartMode
import qt_material
from pathlib import Path
from qt_material_icons import MaterialIcon
from nv200widget import NV200Widget
import PySide6QtAds as QtAds
import qdarktheme


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_mainwindow import Ui_MainWindow



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

        # Create the dock manager. Because the parent parameter is a QMainWindow
        # the dock manager registers itself as the central widget.
        self.dock_manager = QtAds.CDockManager(self)
        self.dock_manager.setStyleSheet("")
        ui.actionAdd_NV200_View.triggered.connect(self.add_nv200_view)
        self.add_nv200_view()


    def add_nv200_view(self):
        """
        Adds a new NV200 view to the main window.
        """
        nv200widget = NV200Widget(self)
        dock_widget = QtAds.CDockWidget("NV200")
        dock_widget.setWidget(nv200widget)
        #nv200widget.status_message.connect(self.statusBar().showMessage)
        #self.setCentralWidget(nv200widget)
        # Add the dock widget to the top dock widget area
        self.dock_manager.addDockWidget(QtAds.RightDockWidgetArea, dock_widget)

   
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

def set_dark_fusion_style(app : QApplication):
    """
    Sets the application style to a dark fusion theme.
    """
    QApplication.setStyle('Fusion')
    QApplication.setPalette(QApplication.style().standardPalette())
    dark_palette = QApplication.palette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    QApplication.setPalette(dark_palette)


if __name__ == "__main__":
    setup_logging()
    app = QApplication(sys.argv)
    app_path = Path(__file__).resolve().parent
    app.setWindowIcon(QIcon(str(app_path) + '/app_icon.ico'))
    #set_dark_fusion_style(app)
    #qt_material.apply_stylesheet(app, theme='dark_teal.xml')

    qdarktheme.setup_theme(theme="dark", custom_colors={"primary": "#00C267"})
    palette = qdarktheme.load_palette(theme="dark", custom_colors={"primary": "#00C267"})
    app.setPalette(palette)

    #print(qdarktheme.load_stylesheet(theme="dark", custom_colors={"primary": "#00C267"}))


    widget = MainWindow()
    widget.show()
    #sys.exit(app.exec())
    with qtinter.using_asyncio_from_qt():
        app.exec()
