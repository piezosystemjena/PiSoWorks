from enum import Enum
import traceback
from functools import wraps
from typing import Any, Callable, Awaitable
from pathlib import Path
from qt_material_icons import MaterialIcon
from PySide6.QtCore import QObject
from PySide6.QtGui import QPalette, QIcon, QPixmap, QAction
from PySide6.QtWidgets import QComboBox, QMessageBox, QStyle, QWidget
import qtinter


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
    icon.set_color(QPalette().color(color))
    return icon


def get_icon_for_menu(icon_name: str, size: int = 24, fill: bool = True, color : QPalette.ColorRole = QPalette.ColorRole.Highlight) -> MaterialIcon:
    """
    Returns the icon of the given QMenu, if it has one.

    Args:
        menu (QMenu): The QMenu instance to retrieve the icon from.

    Returns:
        QIcon | None: The icon of the menu, or None if not set.
    """
    icon = get_icon(icon_name, size=size, fill=fill, color=color)
    icon.set_color(QPalette().color(QPalette.ColorRole.Window), QIcon.Mode.Active)
    return icon


def set_combobox_index_by_value(combo: QComboBox, value: Any) -> None:
    """
    Sets the current index of the QComboBox to the item with the given userData value.

    Args:
        combo: The QComboBox instance.
        value: The value to match in userData of combo items.
    """
    expected_type: type = None

    # Get the first element to fetch the type
    if combo.count() > 0:
        expected_type = type(combo.itemData(0))

    # If combobox expects Enum but new value is not Enum, create Enum
    try:
        if issubclass(expected_type, Enum) and not issubclass(type(value), Enum):   
            value = value_to_enum(expected_type, value)
    except ValueError:
        raise ValueError(f"Value {value!r} not found in QComboBox.")

    index: int = combo.findData(value)
    if index != -1:
        combo.setCurrentIndex(index)
    else:
        raise ValueError(f"Value {value!r} not found in QComboBox.")
    
    
def get_enum_value_type(enum: Enum) -> type | None:
    """
    Retrieves the type of the underlying values in an Enum class.

    Args:
        enum (Enum): The Enum class to inspect.

    Returns:
        type | None: The type of the first enum value, or None if the enum has no values.
    """
    tmp = [e.value for e in enum]

    # If any value exists, return the type of the first value
    if len(tmp) > 0:
        return type(tmp[0])
    
    return None
    
def value_to_enum(enum: Enum, val) -> Enum:
    """
    Converts a raw value to its corresponding Enum member by casting the value to the enum's underlying type.

    Args:
        enum (Enum): The Enum class to convert the value to.
        val: The raw value to convert to an enum member.

    Returns:
        Enum: The enum member corresponding to the converted value.
    """
    enum_type: type = get_enum_value_type(enum)

    if enum_type is None:
        raise ValueError(f"Enum {enum} has no values.")

    return enum(enum_type(val))

def images_path() -> Path:
    """
    Returns the absolute path to the images directory within the current module.

    This function constructs the path based on the location of this file and returns it as a Path object.
    """
    base_dir = Path(__file__).parent
    return base_dir / "assets" / "images"


def safe_asyncslot(coro_func: Callable[..., Awaitable], handler=None):
    """
    Wrap qtinter.asyncslot to catch exceptions from async slots.

    Example:
        >>> ui.searchDevicesButton.clicked.connect(safe_asyncslot(self.search_all_devices))
    """
    if handler is None:
        handler = default_exception_handler

    @wraps(coro_func)
    async def wrapper(*args, **kwargs):
        try:
            return await coro_func(*args, **kwargs)
        except Exception as e:
            handler(e)

    return qtinter.asyncslot(wrapper)


def default_exception_handler(exc: BaseException):
    """
    Handles uncaught exceptions by printing the traceback to the console and displaying a critical error message box.

    Args:
        exc (BaseException): The exception instance to handle.

    Side Effects:
        - Prints the full traceback of the exception to the standard output.
        - Displays a critical QMessageBox with the exception message.
    """
    tb = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    print("Unhandled Exception:\n", tb)
    QMessageBox.critical(None, "Unhandled Exception", str(exc))


def repolish(w : QWidget):
    """
    Calls unpolish() / polish for the style of the given widget to update
    stylesheet if a property changes
    """
    w.style().unpolish(w)
    w.style().polish(w)


def company_logo_pixmap(dark_theme : bool) -> QPixmap :
    """
    Returns a QPixmap object containing the company logo image, selecting the appropriate version for dark or light themes.

    Args:
        dark_theme (bool): If True, returns the logo suitable for dark themes; otherwise, returns the logo for light themes.

    Returns:
        QPixmap: The pixmap containing the company logo image.
    """
    if dark_theme:
        image_file = "piezosystem_logo_white@2x.png"
    else:
        image_file = "piezosystem_logo@2x.png"
    image_path = images_path() / image_file
    return QPixmap(str(image_path))


def menu_separator(parent : QObject | None) -> QAction:
    """
    Creates and returns a QAction that serves as a separator in menus.

    Returns:
        QAction: A QAction configured as a separator.
    """
    sep = QAction(parent)
    sep.setSeparator(True)
    return sep
