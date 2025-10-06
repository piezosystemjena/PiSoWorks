import threading
import os
from typing import Optional, Type
from PySide6.QtCore import QSettings, QStandardPaths


# Get the recommended config directory for the user
config_dir: str = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)

# Ensure the directory exists
os.makedirs(config_dir, exist_ok=True)

# Define the full path to your settings INI file
ini_file_path: str = os.path.join(config_dir, "settings.ini")
print(f"INI file path: {ini_file_path}")


_settings: Optional[QSettings] = None
_settings_lock: threading.RLock = threading.RLock()



def get_settings() -> QSettings:
    """
    Lazily create and return the global QSettings instance.

    Must be called after QCoreApplication is initialized and
    application/org names are set.

    Returns:
        QSettings: The global QSettings instance using INI format and
                   application-specific config path.
    """
    global _settings
    if _settings is None:
        # Retrieve the app config path (now with correct app/org info)
        config_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
        os.makedirs(config_dir, exist_ok=True)
        ini_file_path = os.path.join(config_dir, "settings.ini")
        print(f"Creating QSettings with INI file path: {ini_file_path}")
        _settings = QSettings(ini_file_path, QSettings.Format.IniFormat)
    return _settings



class SettingsContext:
    """
    Thread-safe context manager providing exclusive access
    to the lazily initialized global QSettings instance.
    """

    def __enter__(self) -> QSettings:
        _settings_lock.acquire()
        return get_settings()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> bool:
        try:
            get_settings().sync()
        finally:
            _settings_lock.release()
        return False

