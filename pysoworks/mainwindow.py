# This Python file uses the following encoding: utf-8
import sys
import asyncio
import logging
import os

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import (
    Qt,
    QDir,
    QCoreApplication,
    QSize,
    QObject,
    QtMsgType,
    qInstallMessageHandler,
    qDebug,
)
from PySide6.QtGui import QColor, QIcon, QPalette
from PySide6.QtWidgets import QDoubleSpinBox
import qtinter
import qt_material
from pathlib import Path
from qt_material_icons import MaterialIcon
from nv200widget import NV200Widget
from spiboxwidget import SpiBoxWidget
import PySide6QtAds as QtAds
import qdarktheme
from rich.traceback import install as install_rich_traceback
from rich.logging import RichHandler


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
from ui_mainwindow import Ui_MainWindow



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
        self.setWindowTitle("PySoWorks")
        ui = self.ui
        ui.setupUi(self)

        # Create the dock manager. Because the parent parameter is a QMainWindow
        # the dock manager registers itself as the central widget.
        self.dock_manager = QtAds.CDockManager(self)
        self.dock_manager.setStyleSheet("")
        ui.actionAdd_NV200_View.triggered.connect(self.add_nv200_view)
        ui.actionAdd_SpiBox_View.triggered.connect(self.add_spibox_view)
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
        widget.status_message.connect(self.statusBar().showMessage)


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


def set_qdarktheme_style(app: QApplication):
    """
    Applies a custom QDarkTheme dark style to the given QApplication instance.
    This function sets up the application's theme using QDarkTheme with a custom primary color and sharp corners.
    It loads and applies a custom palette and, if a 'dark_theme.css' stylesheet exists in the application path,
    applies it as the application's stylesheet.
    """
    qdarktheme.setup_theme(theme="dark", custom_colors={"primary": "#00C267"}, corner_shape="sharp")
    palette = qdarktheme.load_palette(theme="dark", custom_colors={"primary": "#00C267"})
    app.setPalette(palette)

    dark_theme = qdarktheme.load_stylesheet(theme="dark", custom_colors={"primary": "#00C267"})
    #print("\n\n" + dark_theme + "\n\n")
    stylesheet_path = app_path / 'dark_theme.css'
    if stylesheet_path.exists():
        with open(stylesheet_path, "r") as f:
            stylesheet = f.read()
            #print(f"StyleSheet: {stylesheet}")
            app.setStyleSheet(stylesheet)


def set_qt_material_style(app: QApplication):
    """
    Applies the Qt Material stylesheet with the 'dark_teal' theme to the given QApplication instance.
    """
    extra = {
        # Density Scale
        'density_scale': '-2',
    }
    qt_material.apply_stylesheet(app, theme='dark_teal.xml', extra=extra)


if __name__ == "__main__":
    setup_logging()
    app = QApplication(sys.argv)
    app_path = Path(__file__).resolve().parent
    app.setWindowIcon(QIcon(str(app_path) + '/app_icon.ico'))
    #set_dark_fusion_style(app)
    #set_qt_material_style(app)
    set_qdarktheme_style(app)
    widget = MainWindow()
    widget.show()
    #sys.exit(app.exec())
    with qtinter.using_asyncio_from_qt():
        app.exec()
