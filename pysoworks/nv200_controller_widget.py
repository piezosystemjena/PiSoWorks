from pathlib import Path
from PySide6.QtWidgets import QFrame
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPainter
from PySide6.QtCore import QSize, QRect, Signal, Qt

from pysoworks.ui_nv200_controller_widget import Ui_nv200ControllerWidget



class Nv200ControllerWidget(QFrame):

    status_message = Signal(str, int)  # message text, timeout in ms   

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_nv200ControllerWidget()
        ui = self.ui
        ui.setupUi(self)
        base_dir = Path(__file__).parent
        svg_path = base_dir / "assets" / "images" / "nv200_controller_structure.svg"
        self.ui.controllerStrcutureFrame.setStyleSheet(""
            "#controllerStrcutureFrame {"
            "background-image: url(:/assets/images/nv200_controller_structure.svg) no-repeat left top;"
            "}"
        )
        #self.svg_renderer = QSvgRenderer(str(svg_path))  # Replace with your SVG file path
        #self.svg_renderer.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

        # Optional: Set a fixed widget size or minimum size
        #self.setMinimumSize(self.svg_renderer.defaultSize)  # Give some padding around the SVG if

    # def paintEvent(self, event):
    #     painter = QPainter(self)

    #     fixed_size = self.svg_renderer.defaultSize()
    #     target_rect = QRect(0, 0, fixed_size.width(), fixed_size.height())

    #     self.svg_renderer.render(painter, target_rect)

    #     super().paintEvent(event)

