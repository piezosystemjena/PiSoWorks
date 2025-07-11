# This Python file uses the following encoding: utf-8
import sys
import logging
from typing import List, Dict
import json
import pkgutil
import os


from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import (
    Qt,
    QtMsgType,
    qInstallMessageHandler,
    QStandardPaths,
)
from PySide6.QtGui import QIcon, QGuiApplication

import qtinter
from pathlib import Path
import PySide6QtAds as QtAds
import qtass
from rich.traceback import install as install_rich_traceback
from rich.logging import RichHandler

from pysoworks.nv200widget import NV200Widget
from pysoworks.spiboxwidget import SpiBoxWidget
from pysoworks.nv200_controller_widget import Nv200ControllerWidget

def qt_message_handler(mode, context, message):
    if mode == QtMsgType.QtDebugMsg:
        print(f"[QtDebug] {message}")
    elif mode == QtMsgType.QtInfoMsg:
        print(f"[QtInfo] {message}")
    elif mode == QtMsgType.QtWarningMsg:
        print(f"[QtWarning] {message}")
    elif mode == QtMsgType.QtCriticalMsg:
        print(f"[QtCritical] {message}")
    elif mode == QtMsgType.QtFatalMsg:
        print(f"[QtFatal] {message}")

qInstallMessageHandler(qt_message_handler)


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from pysoworks.ui_mainwindow import Ui_MainWindow



class MainWindow(QMainWindow):
    """
    Main application window for the PySoWorks UI, providing asynchronous device discovery, connection, and control features.
    Attributes:
        _device (DeviceClient): The currently connected device client, or None if not connected.
        _recorder (DataRecorder): The data recorder associated with the connected device, or None if not initialized
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        ui = self.ui
        ui.setupUi(self)

        # Create the dock manager. Because the parent parameter is a QMainWindow
        # the dock manager registers itself as the central widget.
        self.dock_manager = QtAds.CDockManager(self)
        self.dock_manager.setStyleSheet("")
        ui.actionNv200View.triggered.connect(self.add_nv200_view)
        ui.actionSpiBoxView.triggered.connect(self.add_spibox_view)
        self.add_nv200_view()

    def add_view(self, widget_class, title):
        """
        Adds a new view to the main window.
        :param widget_class: The class of the widget to be added.
        :param title: The title of the dock widget.
        """
        widget = widget_class(self)
        dock_widget = QtAds.CDockWidget(title)
        dock_widget.setWidget(widget)
        self.dock_manager.addDockWidget(QtAds.RightDockWidgetArea, dock_widget)
        widget.status_message.connect(self.show_status_message)


    def add_nv200_view(self):
        """
        Adds a new NV200 view to the main window.
        """
        self.add_view(NV200Widget, "NV200")

    def add_spibox_view(self):
        """
        Adds a new SpiBox view to the main window.
        """
        self.add_view(SpiBoxWidget, "SpiBox")


    def show_status_message(self, message: str, timeout: int | None = 4000):
        """
        Displays a status message in the status bar.
        :param message: The message to display.
        """
        if message.startswith("Error"):
            self.statusBar().setStyleSheet("QStatusBar { color: red; }")
        else:
            self.statusBar().setStyleSheet("")
        self.statusBar().showMessage(message, timeout)

   
def setup_logging():
    """
    Configures the logging settings for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d | %(name)-25s | %(message)s',
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, )]
    )
    install_rich_traceback(show_locals=True)  

    logging.getLogger("nv200.device_discovery").setLevel(logging.DEBUG)
    logging.getLogger("nv200.transport_protocols").setLevel(logging.DEBUG)         
    logging.getLogger("nv200.serial_protocol").setLevel(logging.DEBUG)    
    logging.getLogger("nv200.device_base").setLevel(logging.DEBUG)     


def set_qtass_style(app: QApplication):
    """
    Applies the QtAss stylesheet with the 'dark_teal' theme to the given QApplication instance.
    """
    QApplication.setStyle('Fusion')
    stylesheet = qtass.QtAdvancedStylesheet()
    app_path = Path(__file__).resolve().parent
    stylesheet.output_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation) + "/styles"
    stylesheet.set_styles_dir_path(app_path / 'styles')
    stylesheet.set_current_style("metro")
    stylesheet.set_current_theme("piezosystem")
    stylesheet.update_stylesheet()
    app.setStyleSheet(stylesheet.stylesheet)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = ''
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = Path(__file__).resolve().parent.parent
    print(f"base_path: {base_path}")
    return os.path.join(base_path, relative_path)


def main():
    """
    Initializes and runs the main application window.
    """
    setup_logging()
    QGuiApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QGuiApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    QApplication.setDesktopSettingsAware(True)

    QApplication.setEffectEnabled(Qt.UIEffect.UI_AnimateMenu, False)
    QApplication.setEffectEnabled(Qt.UIEffect.UI_AnimateCombo, False)

    app = QApplication(sys.argv)
    app.setApplicationName('PySoWorks')
    app.setApplicationDisplayName('PySoWorks')
    app.setOrganizationName('piezosystem jena')
    app.setOrganizationDomain('piezosystem.com')
    app_path = Path(__file__).resolve().parent
    print(f"Application Path: {app_path}")
    app.setWindowIcon(QIcon(resource_path('pysoworks/assets/app_icon.ico')))
    set_qtass_style(app)

    widget = MainWindow()
    widget.show()
    widget.setWindowTitle('PySoWorks')
    with qtinter.using_asyncio_from_qt():
        app.exec()
