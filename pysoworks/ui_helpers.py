from typing import Any

from qt_material_icons import MaterialIcon
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QComboBox


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


def set_combobox_index_by_value(combo: QComboBox, value: Any) -> None:
    """
    Sets the current index of the QComboBox to the item with the given userData value.

    Args:
        combo: The QComboBox instance.
        value: The value to match in userData of combo items.
    """
    index: int = combo.findData(value)
    if index != -1:
        combo.setCurrentIndex(index)
    else:
        raise ValueError(f"Value {value!r} not found in QComboBox.")