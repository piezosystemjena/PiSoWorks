# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AboutDialog.ui'
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

class Ui_CAboutDialogClass(object):
    def setupUi(self, CAboutDialogClass):
        if not CAboutDialogClass.objectName():
            CAboutDialogClass.setObjectName(u"CAboutDialogClass")
        CAboutDialogClass.resize(716, 290)
        self.verticalLayout = QVBoxLayout(CAboutDialogClass)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.applicationLogoLabel = QLabel(CAboutDialogClass)
        self.applicationLogoLabel.setObjectName(u"applicationLogoLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applicationLogoLabel.sizePolicy().hasHeightForWidth())
        self.applicationLogoLabel.setSizePolicy(sizePolicy)
        self.applicationLogoLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.applicationLogoLabel)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.applicationLabel = QLabel(CAboutDialogClass)
        self.applicationLabel.setObjectName(u"applicationLabel")

        self.verticalLayout_2.addWidget(self.applicationLabel)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.versionLabel = QLabel(CAboutDialogClass)
        self.versionLabel.setObjectName(u"versionLabel")

        self.verticalLayout_2.addWidget(self.versionLabel)

        self.qtVersionLabel = QLabel(CAboutDialogClass)
        self.qtVersionLabel.setObjectName(u"qtVersionLabel")

        self.verticalLayout_2.addWidget(self.qtVersionLabel)

        self.licenseLabel = QLabel(CAboutDialogClass)
        self.licenseLabel.setObjectName(u"licenseLabel")

        self.verticalLayout_2.addWidget(self.licenseLabel)

        self.verticalSpacer_3 = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.copyrightLabel = QLabel(CAboutDialogClass)
        self.copyrightLabel.setObjectName(u"copyrightLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.copyrightLabel.sizePolicy().hasHeightForWidth())
        self.copyrightLabel.setSizePolicy(sizePolicy1)
        self.copyrightLabel.setMinimumSize(QSize(300, 0))
        self.copyrightLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.copyrightLabel)

        self.thirdPartyLicensesLabel = QLabel(CAboutDialogClass)
        self.thirdPartyLicensesLabel.setObjectName(u"thirdPartyLicensesLabel")
        self.thirdPartyLicensesLabel.setTextFormat(Qt.RichText)
        self.thirdPartyLicensesLabel.setOpenExternalLinks(True)
        self.thirdPartyLicensesLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.verticalLayout_2.addWidget(self.thirdPartyLicensesLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.visitLabel = QLabel(CAboutDialogClass)
        self.visitLabel.setObjectName(u"visitLabel")
        sizePolicy.setHeightForWidth(self.visitLabel.sizePolicy().hasHeightForWidth())
        self.visitLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.visitLabel)

        self.urlLabel = QLabel(CAboutDialogClass)
        self.urlLabel.setObjectName(u"urlLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.urlLabel.sizePolicy().hasHeightForWidth())
        self.urlLabel.setSizePolicy(sizePolicy2)
        self.urlLabel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.urlLabel.setOpenExternalLinks(True)
        self.urlLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.horizontalLayout_2.addWidget(self.urlLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.organizationLogoLabel = QLabel(CAboutDialogClass)
        self.organizationLogoLabel.setObjectName(u"organizationLogoLabel")

        self.verticalLayout_2.addWidget(self.organizationLogoLabel)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(CAboutDialogClass)

        QMetaObject.connectSlotsByName(CAboutDialogClass)
    # setupUi

    def retranslateUi(self, CAboutDialogClass):
        CAboutDialogClass.setWindowTitle(QCoreApplication.translate("CAboutDialogClass", u"CAboutDialog", None))
        self.applicationLogoLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"ApplicationLogo", None))
        self.applicationLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"QmixElemnts", None))
        self.versionLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"Version:", None))
        self.qtVersionLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"Based on", None))
        self.licenseLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"License:", None))
        self.copyrightLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"Copyright", None))
        self.thirdPartyLicensesLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"Licenses", None))
        self.visitLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"Visit:", None))
        self.urlLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"http://www.google.de", None))
        self.organizationLogoLabel.setText(QCoreApplication.translate("CAboutDialogClass", u"OrganizationLogo", None))
    # retranslateUi

