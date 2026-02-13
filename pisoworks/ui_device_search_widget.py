# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'device_search_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QPushButton,
    QSizePolicy, QToolButton, QWidget)

class Ui_DeviceSearchWidget(object):
    def setupUi(self, DeviceSearchWidget):
        if not DeviceSearchWidget.objectName():
            DeviceSearchWidget.setObjectName(u"DeviceSearchWidget")
        DeviceSearchWidget.resize(624, 300)
        self.horizontalLayout = QHBoxLayout(DeviceSearchWidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.devicesComboBox = QComboBox(DeviceSearchWidget)
        self.devicesComboBox.setObjectName(u"devicesComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devicesComboBox.sizePolicy().hasHeightForWidth())
        self.devicesComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.devicesComboBox)

        self.searchDevicesButton = QToolButton(DeviceSearchWidget)
        self.searchDevicesButton.setObjectName(u"searchDevicesButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.searchDevicesButton.sizePolicy().hasHeightForWidth())
        self.searchDevicesButton.setSizePolicy(sizePolicy1)
        self.searchDevicesButton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.searchDevicesButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.searchDevicesButton.setProperty(u"alignedWithEdit", True)

        self.horizontalLayout.addWidget(self.searchDevicesButton)

        self.connectionButton = QPushButton(DeviceSearchWidget)
        self.connectionButton.setObjectName(u"connectionButton")
        self.connectionButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.connectionButton.sizePolicy().hasHeightForWidth())
        self.connectionButton.setSizePolicy(sizePolicy1)
        self.connectionButton.setProperty(u"alignedWithEdit", True)

        self.horizontalLayout.addWidget(self.connectionButton)


        self.retranslateUi(DeviceSearchWidget)

        QMetaObject.connectSlotsByName(DeviceSearchWidget)
    # setupUi

    def retranslateUi(self, DeviceSearchWidget):
#if QT_CONFIG(tooltip)
        self.devicesComboBox.setToolTip(QCoreApplication.translate("DeviceSearchWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">Device List</span></p><p>List of detected NV200 devices.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.searchDevicesButton.setToolTip(QCoreApplication.translate("DeviceSearchWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">Search Devices</span></p><p>Search for all NV200 devices connected via USB or Ethernet. Click the menu button to search only USB or only Ethernet devices.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.searchDevicesButton.setText(QCoreApplication.translate("DeviceSearchWidget", u"Search Devices ...", None))
        self.searchDevicesButton.setProperty(u"style", QCoreApplication.translate("DeviceSearchWidget", u"pushButton", None))
#if QT_CONFIG(tooltip)
        self.connectionButton.setToolTip(QCoreApplication.translate("DeviceSearchWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">Connect</span></p><p>Connect to the device you selected from the list.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.connectionButton.setText(QCoreApplication.translate("DeviceSearchWidget", u"Connect", None))
        pass
    # retranslateUi

