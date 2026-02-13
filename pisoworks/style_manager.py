import qtass
from typing import cast
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QStandardPaths
from pisoworks.settings_manager import SettingsContext

class StyleManager:
    """
    A global action manager to decouple widgets from the main window.
    Allows widgets to register actions without directly importing or
    referencing the QMainWindow, avoiding circular imports.
    """

    def __init__(self) -> None:
        QApplication.setStyle('Fusion')
        self.style = qtass.QtAdvancedStylesheet()
        self.default_base_font_size = 9.0
        self.min_base_font_size = 7.0
        self.max_base_font_size = 24.0
        self.base_font_size_step = 1.0
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
            base_font_size = cast(float, settings.value("style/baseFontSize", self.default_base_font_size, type=float))
        self.set_light_theme(light_theme)
        self.set_base_font_size(base_font_size, store=False)


    def notify_application(self) -> None:
        """
        Notifies the application about style changes.
        This allows existing controls to adapt to dark / or light mode
        """
        self.style.dark_mode_changed.emit(self.style.is_current_theme_dark())


    def base_font_size(self) -> float:
        """
        Returns the current base font size from the theme variables.
        """
        value = self.style.theme_variable_value("baseFontSize")
        try:
            return float(value)
        except (TypeError, ValueError):
            return self.default_base_font_size


    def set_base_font_size(self, size: float, *, store: bool = True) -> None:
        """
        Sets the base font size and updates the stylesheet.

        Args:
            size (float): New base font size in points.
            store (bool): Persist setting to QSettings if True.
        """
        clamped = max(self.min_base_font_size, min(self.max_base_font_size, float(size)))
        self.style.set_theme_variable_value("baseFontSize", str(clamped))
        self.style.update_stylesheet()
        app = QApplication.instance()
        if isinstance(app, QApplication):
            app.setStyleSheet(self.style.stylesheet)
        if store:
            with SettingsContext() as settings:
                settings.setValue("style/baseFontSize", clamped)


    def zoom_in(self) -> None:
        """
        Increase base font size by one step.
        """
        self.set_base_font_size(self.base_font_size() + self.base_font_size_step)


    def zoom_out(self) -> None:
        """
        Decrease base font size by one step.
        """
        self.set_base_font_size(self.base_font_size() - self.base_font_size_step)


    def zoom_reset(self) -> None:
        """
        Reset base font size to default.
        """
        self.set_base_font_size(self.default_base_font_size)


# Global instance of the StyleManager   
style_manager = StyleManager()