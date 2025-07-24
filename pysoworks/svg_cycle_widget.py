from typing import List, Optional, Sequence
from pathlib import Path
from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtCore import Signal, Qt, QRectF, QSize, QEvent, Property
from PySide6.QtGui import QPainter, QMouseEvent, QColor, QPalette
from pysoworks.themed_svg_renderer import ThemedSvgRenderer


class SvgCycleWidget(QFrame):
    """
    A QWidget that displays and cycles through a list of SVG images.

    - Clicking the widget cycles to the next SVG.
    - Maintains the aspect ratio of the SVG when resizing.
    - Provides layout-aware sizing (hasHeightForWidth, sizeHint, etc.).
    - Emits a signal when the current image index changes.
    """

    currentIndexChanged: Signal = Signal(int)
    """Signal emitted when the current SVG index changes."""
    clicked = Signal(int)
    """Signal emitted when the widget is clicked, passing the current index."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the widget with a list of SVG file paths.

        Args:
            svg_paths: List of paths to SVG files.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self.renderers: List[ThemedSvgRenderer] = []
        self.current_index: int = 0
        self._color: QColor = self.palette().color(QPalette.ColorRole.Highlight)


    def set_svg_paths(self, paths: Sequence[Path]) -> None:
        """
        Set or replace the list of SVG file paths to display.

        Args:
            paths: A sequence of Path objects pointing to SVG files.
        """
        self.renderers = [ThemedSvgRenderer(filename=str(path), parent=self) for path in paths]
        self.update_svg_colors()

        self.current_index = 0
        if not self.renderers[0].isValid():
            raise ValueError(f"Invalid SVG file: {paths[0]}")

        self.setFixedSize(self.renderers[0].defaultSize())
        self.updateGeometry()
        self.update()
        self.currentIndexChanged.emit(self.current_index)


    def current_renderer(self) -> Optional[ThemedSvgRenderer]:
        """
        Get the QSvgRenderer for the currently active SVG.

        Returns:
            The active renderer, or None if there are no SVGs.
        """
        if not self.renderers:
            return None
        return self.renderers[self.current_index]


    def aspect_ratio(self) -> float:
        """
        Compute the aspect ratio (width / height) of the current SVG.

        Returns:
            The aspect ratio of the SVG, or 1.0 as fallback.
        """
        renderer = self.current_renderer()
        if renderer:
            size = renderer.defaultSize()
            if size.height() != 0:
                return size.width() / size.height()
        return 1.0


    def hasHeightForWidth(self) -> bool:
        """
        Indicate that the widget’s height depends on its width.

        Returns:
            True, since the widget preserves aspect ratio.
        """
        return True


    def heightForWidth(self, width: int) -> int:
        """
        Calculate the appropriate height for a given width based on SVG aspect ratio.

        Args:
            width: The available width.

        Returns:
            The corresponding height maintaining aspect ratio.
        """
        return int(width / self.aspect_ratio())

    def sizeHint(self) -> QSize:
        """
        Provide a recommended default size for the widget.

        Returns:
            The suggested size from the current SVG, or a fallback size.
        """
        renderer = self.current_renderer()
        if renderer:
            return renderer.defaultSize()
        return QSize(200, 200)


    def minimumSizeHint(self) -> QSize:
        """
        Provide a minimum recommended size for the widget.

        Returns:
            A minimum size.
        """
        return self.sizeHint() or QSize(100, 100)


    def paintEvent(self, event: QEvent) -> None:
        """
        Paint the current SVG centered and scaled in the widget area.

        Args:
            event: The paint event.
        """
        painter = QPainter(self)
        renderer = self.current_renderer()
        if not renderer:
            return

        svg_size: QSize = renderer.defaultSize()
        widget_size: QSize = self.size()

        svg_aspect = svg_size.width() / svg_size.height()
        widget_aspect = widget_size.width() / widget_size.height()

        if svg_aspect > widget_aspect:
            target_width = widget_size.width()
            target_height = target_width / svg_aspect
        else:
            target_height = widget_size.height()
            target_width = target_height * svg_aspect

        x = (widget_size.width() - target_width) / 2
        y = (widget_size.height() - target_height) / 2
        target_rect = QRectF(x, y, target_width, target_height)

        renderer.render(painter, target_rect)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Cycle to the next SVG image when the widget is clicked.

        Args:
            event: The mouse press event.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            # Cycle to next image on click
            if self.renderers:
                next_index = (self.current_index + 1) % len(self.renderers)
                self.set_current_index(next_index)
                self.clicked.emit(next_index)  # Emit clicked signal with current index
        super().mousePressEvent(event)


    def set_current_index(self, index: int) -> None:
        """
        Set the current image index, update display and emit currentChanged signal.

        Args:
            index: The index to set as current image.
        """
        if index < 0 or index >= len(self.renderers):
            return  # Invalid index, do nothing

        if self.current_index == index:
            return  # Same index, no change

        self.current_index = index
        self.update()
        self.currentIndexChanged.emit(self.current_index)

    def get_current_index(self) -> int:
        """
        Get the current image index.

        Returns:
            The index of the currently displayed SVG.
        """
        return self.current_index
    
    def get_color(self) -> QColor:
        """
        Returns the current color of the widget.

        Returns:
            QColor: The current color assigned to the widget.
        """
        return self._color
    

    def update_svg_colors(self) -> None:
        """
        Updates the color of the widget based on the current color property.
        """
        for renderer in self.renderers:
            renderer.add_color_replacement(QColor("#2db159"), self._color)
            renderer.update_svg()
        self.update()  # Trigger repaint if color affects rendering

    def set_color(self, color: QColor) -> None:
        """
        Sets the color of the widget.

        If the new color is different from the current color, updates the internal color,
        emits the colorChanged signal with the new color, and triggers a repaint of the widget.

        Args:
            color (QColor): The new color to set for the widget.
        """
        if self._color == color:
            return
        self._color = color
        self.update_svg_colors()

    color = Property(QColor, get_color, set_color)
    currentIndex = Property(int, get_current_index, set_current_index)