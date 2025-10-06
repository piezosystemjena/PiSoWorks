from PySide6.QtCore import QByteArray, QObject, Slot
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QColor
import re
from typing import Dict, Optional


class ThemedSvgRenderer(QSvgRenderer):
    """
    A QSvgRenderer subclass that allows dynamic color theming by replacing
    colors in the original SVG content using a color mapping dictionary.

    It stores the original SVG data internally as a QByteArray, supports
    color replacement rules, and emits repaintNeeded() after updates.
    """

    def __init__(
        self,
        svg_data: QByteArray = QByteArray(),
        filename: Optional[str] = None,
        parent: Optional[QObject] = None
    ) -> None:
        """
        Initialize the renderer with either SVG data or a filename.

        :param svg_data: SVG content as QByteArray (takes priority if not empty).
        :param filename: Path to an SVG file to load if svg_data is empty.
        :param parent: Optional QObject parent.
        """
        super().__init__(parent)
        self._original_svg_data: QByteArray = QByteArray()
        self._color_replacements: Dict[str, str] = {}

        if not svg_data.isEmpty():
            self.set_svg_data(svg_data)
        elif filename:
            self.load(filename)

    @Slot(str, result=bool)
    def load(self, filename: str) -> bool:
        """
        Load an SVG file and store its contents internally as a QByteArray.

        :param filename: Path to the SVG file.
        :return: True if loading succeeded, False otherwise.
        """
        try:
            with open(filename, "rb") as f:
                data = f.read()
        except Exception as e:
            print(f"Failed to read SVG file: {e}")
            return False    
        return self.set_svg_data(QByteArray(data))

    def set_svg_data(self, svg_data: QByteArray) -> bool:
        """
        Set new SVG content and store it internally.

        :param svg_data: SVG content as QByteArray.
        """
        self._original_svg_data = QByteArray(svg_data)
        return self.update_svg()

    def add_color_replacement(self, source: QColor, target: QColor) -> None:
        """
        Add or update a color replacement mapping.

        :param source: The color to be replaced.
        :param target: The new color to apply.
        """
        self._color_replacements[self._color_to_svg_str(source)] = self._color_to_svg_str(target)

    def add_color_replacements(self, replacements: Dict[QColor, QColor]) -> None:
        """
        Add multiple color replacements at once.

        :param replacements: Dictionary of {source_color: target_color}.
        """
        for source, target in replacements.items():
            self.add_color_replacement(source, target)

    def clear_color_replacements(self) -> None:
        """
        Clear all existing color replacement mappings.
        """
        self._color_replacements.clear()

    def update_svg(self) -> bool:
        """
        Apply the current color replacement mappings to the original SVG data,
        reload the modified SVG, and emit repaintNeeded().
        """
        if not self._color_replacements:
            success = super().load(self._original_svg_data)
        else:
            svg_text = self._original_svg_data.toStdString()
            for source_str, target_str in self._color_replacements.items():
                # Match fill, stroke, and inline CSS style values only
                pattern = rf'(?<=[:"\'\s]){re.escape(source_str)}(?=[;"\'\s])'
                svg_text = re.sub(pattern, target_str, svg_text, flags=re.IGNORECASE)

            updated_data = QByteArray(svg_text.encode("utf-8"))
            success = super().load(updated_data)

        if success:
            self.repaintNeeded.emit()
        
        return success

    @staticmethod
    def _color_to_svg_str(color: QColor) -> str:
        """
        Convert QColor to a lowercase hex string usable in SVG.

        :param color: QColor object.
        :return: Color string in format "#rrggbb".
        """
        return color.name(QColor.NameFormat.HexRgb).lower()
