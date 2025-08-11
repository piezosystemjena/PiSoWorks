import qtass
from typing import cast
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QStandardPaths
from pysoworks.settings_manager import SettingsContext

class StyleManager:
    """
    A global action manager to decouple widgets from the main window.
    Allows widgets to register actions without directly importing or
    referencing the QMainWindow, avoiding circular imports.
    """

    def __init__(self) -> None:
        QApplication.setStyle('Fusion')
        self.style = qtass.QtAdvancedStylesheet()
        app_path = Path(__file__).resolve().parent
        style = self.style
        style.output_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation) + "/styles"
        style.set_styles_dir_path(app_path / 'styles')
        style.set_current_style("metro")
        self.dark_mode = True
        self.style.set_current_theme("dark_piezosystem")


    def __set_light_theme(self, light: bool) -> None:
        """
        Sets the light theme for the application.

        Args:
            light (bool): If True, sets the light theme; otherwise, sets the dark theme.
        """
        print(f"Setting light theme: {light}")
        if light:
            self.style.set_current_theme("light_piezosystem")
        else:
            self.style.set_current_theme("dark_piezosystem")
        self.dark_mode = not light
        self.style.update_stylesheet()
        app = QApplication.instance()
        if isinstance(app, QApplication):
            app.setStyleSheet(self.style.stylesheet)


    def apply_stylesheet(self, app: QApplication) -> None:
        """
        Applies the QtAss stylesheet to the given QApplication instance.
        
        Args:
            app (QApplication): The application instance to apply the stylesheet to.
        """
        style = self.style
        style.update_stylesheet()
        app.setStyleSheet(self.style.stylesheet)


    def set_light_theme(self, light: bool) -> None:
        """
        Sets the light theme for the application.

        Args:
            light (bool): If True, sets the light theme; otherwise, sets the dark theme.
        """
        self.__set_light_theme(light)
        with SettingsContext() as settings:
            settings.setValue("theme/light", light)


    def load_theme_from_settings(self) -> None:
        """
        Loads the theme settings from the QSettings.
        Call this function, if all application settings like organization and application name are set.
        """
        with SettingsContext() as settings:
            light_theme = cast(bool, settings.value("theme/light", False, type=bool))
        self.set_light_theme(light_theme)


    def notify_application(self) -> None:
        """
        Notifies the application about style changes.
        This allows existing controls to adapt to dark / or light mode
        """
        self.style.dark_mode_changed.emit(self.style.is_current_theme_dark())


# Global instance of the StyleManager   
style_manager = StyleManager()