from pathlib import Path
from PySide6.QtWidgets import QFrame
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import QSize, QRect, Signal, Qt, QRectF

from pysoworks.ui_nv200_controller_widget import Ui_nv200ControllerWidget


class Nv200ControllerWidget(QFrame):
    """
    This widget renders an SVG diagram of the NV200 controller with support for high-DPI displays and global opacity.
    It uses an offscreen high-DPI pixmap to avoid blurry rendering when opacity is applied, ensuring sharp visuals
    on all display types.

    Attributes:
        status_message (Signal): Signal emitted with a status message (str) and a timeout (int, ms).

    Args:
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    status_message = Signal(str, int)  # message text, timeout in ms   

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_nv200ControllerWidget()
        ui = self.ui
        ui.setupUi(self)
        base_dir = Path(__file__).parent
        images_path = base_dir / "assets" / "images"
        self.init_svg_background(images_path)
        self.init_svg_toggle_widgets(images_path)


    def init_svg_toggle_widgets(self, images_path):
        """
        Initializes the SVG toggle widgets with paths to the SVG files.

        This method sets up the toggle widgets with the absolute paths to the SVG files 
        for the modsrc and cl toggles. It generates a list of paths for each toggle based 
        on the specified images path.

        Args:
            images_path (Path): The directory path containing the SVG image files.
        """
        svg_paths = [ (images_path / f"modsrc_toggle0{i}.svg").resolve() for i in range(1, 5) ]
        self.ui.modsrcToggleWidget.set_svg_paths(svg_paths)

        svg_paths = [ (images_path / f"cl_toggle0{i}.svg").resolve() for i in range(1, 3) ]
        self.ui.clToggleWidget.set_svg_paths(svg_paths)

    def init_svg_background(self, images_path):
        """
        Initializes the SVG background for the controller widget.

        Loads the SVG file from the specified images path, clears any existing stylesheet 
        (used only for absolute positioning in the designer), and sets up the QSvgRenderer 
        with the SVG file. The aspect ratio mode is set to keep the original aspect ratio.

        Args:
            images_path (Path): The directory path containing the SVG image file.
        """
        svg_path = images_path / "nv200_controller_structure.svg"
        # Clear the stylesheet - it is only used in designer for absolute positioning of
        # widgets in the controller diagramm
        self.setStyleSheet("")
        self.svg_renderer = QSvgRenderer(str(svg_path))  # Replace with your SVG file path
        self.svg_renderer.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)


    def paintEvent(self, event):
        """_
        Paints a high DPI SVG image onto the widget with global opacity.

        Normally the following code would be used to render the SVG directly onto the widget:
        code-block:: python

            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            size = self.svg_renderer.defaultSize()
            painter.setOpacity(0.5)  # 🔸 Apply global opacity
            self.svg_renderer.render(painter, QRectF(0, 0, size.width(), size.height()))

        But this approach can lead to blurry rendering on high DPI displays.
        When you call painter.setOpacity(0.5), Qt internally switches to software-based 
        composition (a transparent paint layer), which often causes the rendered SVG to 
        be rasterized at the logical (lower) resolution, losing the High DPI sharpness.

        To solve this, we render to a high-DPI offscreen pixmap manually, then paint it with opacity
        """
        dpr = self.devicePixelRatioF()
        size = self.svg_renderer.defaultSize()
        size_scaled = size * dpr

        # Create a high DPI pixmap to render the SVG offscreen
        pixmap = QPixmap(size_scaled)
        pixmap.setDevicePixelRatio(dpr)
        pixmap.fill(Qt.transparent)

        # Render SVG into pixmap at native resolution
        pixmap_painter = QPainter(pixmap)
        self.svg_renderer.render(pixmap_painter, QRectF(0, 0, size.width(), size.height()))
        pixmap_painter.end()

        # Paint the pixmap onto the widget with opacity
        painter = QPainter(self)
        painter.setOpacity(0.7)
        painter.drawPixmap(0, 0, pixmap)


    def sizeHint(self):
        """
        Returns the recommended size for the widget.

        This method provides a hint to the layout system about the preferred size of the widget.
        It returns a QSize object with a width and height of 10 pixels each.

        Returns:
            QSize: The recommended size for the widget (10x10 pixels).
        """
        return QSize(10, 10)

    def minimumSizeHint(self):
        return QSize(10, 10)
