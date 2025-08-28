# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(716, 290)
        self.verticalLayout = QVBoxLayout(AboutDialog)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(40, 40, 40, 40)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.applicationLogoLabel = QLabel(AboutDialog)
        self.applicationLogoLabel.setObjectName(u"applicationLogoLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applicationLogoLabel.sizePolicy().hasHeightForWidth())
        self.applicationLogoLabel.setSizePolicy(sizePolicy)
        self.applicationLogoLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout_3.addWidget(self.applicationLogoLabel)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.applicationLabel = QLabel(AboutDialog)
        self.applicationLabel.setObjectName(u"applicationLabel")

        self.verticalLayout_2.addWidget(self.applicationLabel)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.versionLabel = QLabel(AboutDialog)
        self.versionLabel.setObjectName(u"versionLabel")

        self.verticalLayout_2.addWidget(self.versionLabel)

        self.qtVersionLabel = QLabel(AboutDialog)
        self.qtVersionLabel.setObjectName(u"qtVersionLabel")

        self.verticalLayout_2.addWidget(self.qtVersionLabel)

        self.verticalSpacer_3 = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.copyrightLabel = QLabel(AboutDialog)
        self.copyrightLabel.setObjectName(u"copyrightLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.copyrightLabel.sizePolicy().hasHeightForWidth())
        self.copyrightLabel.setSizePolicy(sizePolicy1)
        self.copyrightLabel.setMinimumSize(QSize(300, 0))
        self.copyrightLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.copyrightLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.visitLabel = QLabel(AboutDialog)
        self.visitLabel.setObjectName(u"visitLabel")
        sizePolicy.setHeightForWidth(self.visitLabel.sizePolicy().hasHeightForWidth())
        self.visitLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.visitLabel)

        self.urlLabel = QLabel(AboutDialog)
        self.urlLabel.setObjectName(u"urlLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.urlLabel.sizePolicy().hasHeightForWidth())
        self.urlLabel.setSizePolicy(sizePolicy2)
        self.urlLabel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.urlLabel.setTextFormat(Qt.TextFormat.RichText)
        self.urlLabel.setOpenExternalLinks(True)
        self.urlLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        self.horizontalLayout_2.addWidget(self.urlLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.organizationLogoLabel = QLabel(AboutDialog)
        self.organizationLogoLabel.setObjectName(u"organizationLogoLabel")

        self.verticalLayout_2.addWidget(self.organizationLogoLabel)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(AboutDialog)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"AboutDialog", None))
        self.applicationLogoLabel.setText(QCoreApplication.translate("AboutDialog", u"ApplicationLogo", None))
        self.applicationLabel.setText(QCoreApplication.translate("AboutDialog", u"Application Name", None))
        self.versionLabel.setText(QCoreApplication.translate("AboutDialog", u"Version:", None))
        self.qtVersionLabel.setText(QCoreApplication.translate("AboutDialog", u"Based on", None))
        self.copyrightLabel.setText(QCoreApplication.translate("AboutDialog", u"Copyright", None))
        self.visitLabel.setText(QCoreApplication.translate("AboutDialog", u"Visit:", None))
        self.urlLabel.setText(QCoreApplication.translate("AboutDialog", u"<a href=\"http://www.google.de\">http://www.google.de</a>", None))
        self.organizationLogoLabel.setText(QCoreApplication.translate("AboutDialog", u"OrganizationLogo", None))
    # retranslateUi

