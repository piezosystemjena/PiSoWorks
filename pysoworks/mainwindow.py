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
    qDebug,
    QProcessEnvironment
)
from PySide6.QtGui import QColor, QIcon, QPalette
from PySide6.QtWidgets import QDoubleSpinBox

import qtinter
import qt_material
from pathlib import Path
from qt_material_icons import MaterialIcon
import PySide6QtAds as QtAds
import qdarktheme
from rich.traceback import install as install_rich_traceback
from rich.logging import RichHandler

from pysoworks import assets
from pysoworks.nv200widget import NV200Widget
from pysoworks.spiboxwidget import SpiBoxWidget

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
    logging.getLogger("nv200.device_base").setLevel(logging.DEBUG)     


def set_dark_fusion_style(app : QApplication):
    """
    Sets the application style to a dark fusion theme.
    """
    ROLE_MAP: dict[str, QPalette.ColorRole] = {
        "WindowText": QPalette.WindowText,
        "Button": QPalette.Button,
        "Light": QPalette.Light,
        "Midlight": QPalette.Midlight,
        "Dark": QPalette.Dark,
        "Mid": QPalette.Mid,
        "Text": QPalette.Text,
        "BrightText": QPalette.BrightText,
        "ButtonText": QPalette.ButtonText,
        "Base": QPalette.Base,
        "Window": QPalette.Window,
        "Shadow": QPalette.Shadow,
        "Highlight": QPalette.Highlight,
        "HighlightedText": QPalette.HighlightedText,
        "Link": QPalette.Link,
        "LinkVisited": QPalette.LinkVisited,
        "AlternateBase": QPalette.AlternateBase,
        "NoRole": QPalette.NoRole,
        "ToolTipBase": QPalette.ToolTipBase,
        "ToolTipText": QPalette.ToolTipText,
        "PlaceholderText": QPalette.PlaceholderText,
        "Accent": QPalette.Accent
    }

    def export_palette_to_json(palette):
        # List of tuples (role_name_str, QPalette.ColorRole)
        palette_states = {
            "Active": QPalette.Active,
            "Inactive": QPalette.Inactive,
            "Disabled": QPalette.Disabled,
        }

        output: Dict[str, Dict[str, str]] = {}

        for state_name, state_enum in palette_states.items():
            state_colors: Dict[str, str] = {}
            for role_name, role_enum in ROLE_MAP.items():
                try:
                    color: QColor = palette.color(state_enum, role_enum)
                    state_colors[role_name] = color.name()  # Hex string only
                except Exception:
                    continue
            output[state_name] = state_colors
        print(json.dumps(output, indent=4))

    def load_palette_from_json() -> QPalette:
        # Use this to ensure that it also works with a PyInstaller package
        text = pkgutil.get_data('pysoworks.assets', 'dark_palette.json').decode('utf-8')
        palette_dict: Dict[str, Dict[str, str]] = json.loads(text)

        palette = QPalette()

        state_map: Dict[str, QPalette.ColorGroup] = {
            "Active": QPalette.Active,
            "Inactive": QPalette.Inactive,
            "Disabled": QPalette.Disabled,
        }


        for state_name, colors in palette_dict.items():
                state_enum = state_map.get(state_name)
                if state_enum is None:
                    continue

                for role_name, hex_color in colors.items():
                    role_enum = ROLE_MAP.get(role_name)
                    if role_enum is None:
                        continue

                    color = QColor(hex_color)
                    palette.setColor(state_enum, role_enum, color)

        return palette


    QApplication.setStyle('Fusion')
    dark_palette = load_palette_from_json()
    QApplication.setPalette(dark_palette)
    #export_palette_to_json(QApplication.palette())
    stylesheets: List[str] = []
    stylesheets.append(assets.load_stylesheet('ads_base.qss'))
    stylesheets.append(assets.load_stylesheet('ads_dark.qss'))
    stylesheet='\n'.join(stylesheets)
    app.setStyleSheet(stylesheet)



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
        'density_scale': '-1',
    }
    qt_material.apply_stylesheet(app, theme='dark_teal.xml', extra=extra)


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
    app = QApplication(sys.argv)
    app_path = Path(__file__).resolve().parent
    print(f"Application Path: {app_path}")
    app.setWindowIcon(QIcon(resource_path('pysoworks/assets/app_icon.ico')))

    set_dark_fusion_style(app)
    #set_qt_material_style(app)
    #set_qdarktheme_style(app)

    widget = MainWindow()
    widget.show()
    widget.setWindowTitle('PySoWorks')
    with qtinter.using_asyncio_from_qt():
        app.exec()
