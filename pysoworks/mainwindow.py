# This Python file uses the following encoding: utf-8
import sys
import logging
import os


from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import (
    Qt,
    QtMsgType,
    qInstallMessageHandler,
    QLocale,
    QUrl
)
from PySide6.QtGui import QIcon, QGuiApplication, QAction, QDesktopServices, QPalette

import qtinter
from pathlib import Path
import PySide6QtAds as QtAds
from rich.traceback import install as install_rich_traceback
from rich.logging import RichHandler

from pysoworks.nv200widget import NV200Widget
from pysoworks.spiboxwidget import SpiBoxWidget
from pysoworks.action_manager import ActionManager, MenuID, action_manager
from pysoworks.style_manager import StyleManager, style_manager
from pysoworks.settings_manager import SettingsContext
from pysoworks.about_dialog import AboutDialog
import pysoworks.ui_helpers as ui_helpers


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

        self.init_action_manager() 

        # Create the dock manager. Because the parent parameter is a QMainWindow
        # the dock manager registers itself as the central widget.
        #QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.FocusHighlighting, True)
        QtAds.CDockManager.setAutoHideConfigFlags(QtAds.CDockManager.DefaultAutoHideConfig)
        self.dock_manager = QtAds.CDockManager(self)
        self.dock_manager.setStyleSheet("")
        ui.actionNv200View.triggered.connect(self.add_nv200_view)
        ui.actionNv200View.setIcon(ui_helpers.get_icon_for_menu("add", size=24, fill=False))
        ui.actionSpiBoxView.triggered.connect(self.add_spibox_view)
        ui.actionSpiBoxView.setIcon(ui_helpers.get_icon_for_menu("add", size=24, fill=False))
        self.add_nv200_view()
        self.resize(1600, 900)  # Set initial size to 800x600

        self.init_style_controls()


    def init_action_manager(self):
        """
        Initializes the ActionManager and registers the main window.
        This method should be called after the main window is set up.
        """
        action_manager.register_main_window(self)

        # Register menus
        action_manager.register_menu(MenuID.FILE, self.ui.menuFile)
        action_manager.register_menu(MenuID.VIEW, self.ui.menuView)
        action_manager.register_menu(MenuID.HELP, self.ui.menuHelp)

        manual_action = QAction("Manual...", parent=self)
        manual_action.triggered.connect(self.show_manual)
        manual_action.setIcon(ui_helpers.get_icon_for_menu("book_2", size=24, fill=False))
        action_manager.add_action_to_menu(MenuID.HELP, manual_action)

        help_action = QAction("Online Manual...", parent=self)
        help_action.triggered.connect(self.show_online_manual)
        help_action.setIcon(ui_helpers.get_icon_for_menu("language", size=24, fill=False))
        action_manager.add_action_to_menu(MenuID.HELP, help_action)

        action_manager.add_action_to_menu(MenuID.HELP, ui_helpers.menu_separator(self))

        show_about_dlg_action = QAction("About PySoWorks", parent=self)
        show_about_dlg_action.triggered.connect(self.show_about_dialog)
        show_about_dlg_action.setIcon(QIcon(str(ui_helpers.images_path() / "app_icon.svg")))
        action_manager.add_action_to_menu(MenuID.HELP, show_about_dlg_action)

    def init_style_controls(self):
        """
        Initializes the style controls for the main window.
        This method sets up the UI elements related to styling and appearance.  
        """
        menu = self.ui.menuView
        menu.addSeparator()
        a = self.light_theme_action = QAction("Light Theme", self)
        a.setCheckable(True)
        a.setChecked(not style_manager.style.is_current_theme_dark())
        menu.addAction(a)
        a.triggered.connect(style_manager.set_light_theme)
        

    def add_view(self, widget_class, title) -> QtAds.CDockWidget:
        """
        Adds a new view to the main window.
        :param widget_class: The class of the widget to be added.
        :param title: The title of the dock widget.
        """
        widget = widget_class(self)
        dock_widget = QtAds.CDockWidget(title)
        dock_widget.setWidget(widget)
        dock_widget.setFeature(QtAds.CDockWidget.DockWidgetDeleteOnClose, True)
        self.dock_manager.addDockWidgetTab(QtAds.CenterDockWidgetArea, dock_widget)
        widget.status_message.connect(self.show_status_message)
        dock_widget.closed.connect(widget.cleanup)
        return dock_widget


    def add_nv200_view(self):
        """
        Adds a new NV200 view to the main window.
        """
        dock_widget = self.add_view(NV200Widget, "NV200")

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


    def show_online_manual(self):
        """
        Opens the online manual in the default web browser.
        """
        QDesktopServices.openUrl(QUrl("https://piezosystemjena.github.io/PySoWorks"))

    def show_manual(self):
        """
        Attempts to open the user manual in the default web browser.

        The method first tries to locate the manual in the 'doc/index.html' directory
        relative to the application's executable path. If unsuccessful, it attempts to
        open the manual from 'doc/_build/index.html' relative to the source code location.

        Status messages are displayed with the resolved manual path for debugging purposes.
        """
        base_path = os.path.dirname(sys.executable)
        manual_path = os.path.join(base_path, "doc/index.html")
        if QDesktopServices.openUrl(QUrl.fromLocalFile(manual_path)):
            return
        base_path = Path(__file__).resolve().parent.parent
        manual_path = base_path / "doc/_build/index.html"
        QDesktopServices.openUrl(QUrl.fromLocalFile(manual_path))


    def show_about_dialog(self):
        """
        Displays the About dialog.
        """
        dialog = AboutDialog(self)
        dialog.exec_()

   
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


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = ''
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = Path(__file__).resolve().parent.parent
    print(f"base_path: {base_path}")
    return os.path.join(base_path, relative_path)


class ExceptionCatchingApplication(QApplication):
    """
    A custom QApplication subclass that catches all exceptions occurring during event notification.

    Overrides the `notify` method to wrap event processing in a try-except block. If an exception is raised while processing an event, it is handled by `ui_helpers.default_exception_handler`, and the method returns False to indicate the event was not handled successfully.

    This helps prevent unhandled exceptions from crashing the application and provides a centralized place for exception handling in the Qt event loop.

    Methods
    -------
    notify(receiver, event)
        Processes the event for the given receiver, catching and handling any exceptions that occur.
    """
    def __init__(self, argv: list[str]) -> None:
        """
        Initialize the application and set the global exception hook.
        """
        super().__init__(argv)
        sys.excepthook = self.handle_exception


    def notify(self, receiver, event):
        """
        Overrides QApplication.notify to catch exceptions during event delivery.
        """
        try:
            return super().notify(receiver, event)
        except Exception as e:
            ui_helpers.default_exception_handler(e)
            return False
        
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """
        Central handler for uncaught exceptions.
        """
        ui_helpers.default_exception_handler(exc_value)
        # Optional: also print the traceback
        import traceback
        traceback.print_exception(exc_type, exc_value, exc_traceback)



def main():
    """
    Initializes and runs the main application window.
    """
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
    setup_logging()
    QGuiApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QGuiApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    QApplication.setDesktopSettingsAware(True)

    QApplication.setEffectEnabled(Qt.UIEffect.UI_AnimateMenu, False)
    QApplication.setEffectEnabled(Qt.UIEffect.UI_AnimateCombo, False)

    app = ExceptionCatchingApplication(sys.argv)
    app.setApplicationName('PySoWorks')
    app.setOrganizationName('piezosystem jena')
    app.setOrganizationDomain('https://www.piezosystem.com/')
    version = Path(resource_path("VERSION")).read_text(encoding="utf-8").strip()
    app.setApplicationVersion(version)
    print(f"PySoWorks Version: {version}")
    app.setApplicationDisplayName(f'PySoWorks {version}')
    app_path = Path(__file__).resolve().parent
    print(f"Application Path: {app_path}")
    app.setWindowIcon(QIcon(resource_path('pysoworks/assets/app_icon.ico')))
    style_manager.load_theme_from_settings()

    widget = MainWindow()
    widget.show()
    widget.setWindowTitle(app.applicationDisplayName())

    style_manager.notify_application()

    with qtinter.using_asyncio_from_qt():
        app.exec()
