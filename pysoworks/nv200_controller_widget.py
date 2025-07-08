from pathlib import Path
from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import QSize, Signal

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
        self.init_png_background(images_path)
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
        self.ui.modsrcToggleWidget.setStyleSheet("")

        svg_paths = [ (images_path / f"cl_toggle0{i}.svg").resolve() for i in range(1, 3) ]
        self.ui.clToggleWidget.set_svg_paths(svg_paths)
        self.ui.clToggleWidget.setStyleSheet("")


    def init_png_background(self, images_path):
        """
        Initializes the PNG background for the controller widget.
        """
        png_path = images_path / "nv200_controller_structure@2x.png"
        self.setStyleSheet("")
        self.background_pixmap = QPixmap(str(png_path))


    def paintEvent(self, event):
        """
        Paints the PNG image directly onto the widget with global opacity.
        """
        if self.background_pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(0.7)

        painter.drawPixmap(0, 0, self.background_pixmap)


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
