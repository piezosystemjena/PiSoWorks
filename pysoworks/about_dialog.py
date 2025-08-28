# about_dialog.py
from PySide6.QtWidgets import QDialog, QLayout, QApplication
from PySide6.QtGui import QPixmap, QIcon, QPalette
from PySide6.QtCore import QDate, Qt, QSize, QUrl
import PySide6
import sys
import pysoworks.ui_helpers as ui_helpers

from pysoworks.ui_about_dialog import Ui_AboutDialog
from pysoworks.style_manager import style_manager

class AboutDialog(QDialog):
    """
    A classical About dialog to display application information such as
    application name, version, organization name, logos, and license info.
    """

    def __init__(self, parent=None) -> None:
        """
        Initialize the About dialog.

        Args:
            parent (QWidget | None): Parent widget.
            app (QApplication | None): Reference to the application instance
                which should provide the following attributes:
                - applicationName()
                - applicationVersion()
                - organizationName()
                - organizationDomain()
                - thirdPartyLicensesUrl()
                - licenseManager.activeLicenseKey().versionTypeString()
        """
        super().__init__(parent)
        self.ui: Ui_AboutDialog = Ui_AboutDialog()
        self.ui.setupUi(self)

        # Set default logos
        self._setup_default_logos()

        # Populate labels with app info
        self._populate_info()

        # Ensure dialog has fixed size
        if self.layout() is not None:
            self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        ui = self.ui
        ui.urlLabel.setTextFormat(Qt.TextFormat.RichText)
        ui.urlLabel.setOpenExternalLinks(True)
        ui.urlLabel.linkActivated.connect(lambda: print("URL clicked"))

    def _setup_default_logos(self) -> None:
        """Set the default application and organization logos."""
        app_icon = QIcon(str(ui_helpers.images_path() / "app_icon_brand.svg"))
        org_pixmap = ui_helpers.company_logo_pixmap(style_manager.dark_mode)

        self.ui.applicationLogoLabel.setPixmap(app_icon.pixmap(QSize(192, 192)))
        self.ui.organizationLogoLabel.setPixmap(org_pixmap)

    def _populate_info(self) -> None:
        """Populate all labels with information from the application."""
        app = QApplication.instance()
        if app is None:
            return
        
        ui = self.ui
        
        ui.applicationLabel.setText(app.applicationName())

        # Version info
        ui.versionLabel.setText(f"Version: {app.applicationVersion()}")
        ui.qtVersionLabel.setText(f"Based on PySide: {PySide6.__version__}")


        # Organization info
        ui.urlLabel.setText(f"<a href=\"{app.organizationDomain()}\">{app.organizationDomain()}</a>")
        ui.urlLabel.setTextFormat(Qt.TextFormat.RichText)
        ui.urlLabel.setOpenExternalLinks(True)
        current_year = QDate.currentDate().toString("yyyy")
        ui.copyrightLabel.setText(
            f"© Copyright {current_year} {app.organizationName()}. All rights reserved."
        )

    # Properties for logos
    def set_application_logo(self, logo: QPixmap) -> None:
        """Set the application logo."""
        self.ui.applicationLogoLabel.setPixmap(logo)

    def application_logo(self) -> QPixmap | None:
        """Return the current application logo."""
        return self.ui.applicationLogoLabel.pixmap()

    def set_organization_logo(self, logo: QPixmap) -> None:
        """Set the organization logo."""
        self.ui.organizationLogoLabel.setPixmap(logo)

    def organization_logo(self) -> QPixmap | None:
        """Return the current organization logo."""
        return self.ui.organizationLogoLabel.pixmap()