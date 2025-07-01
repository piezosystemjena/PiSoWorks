# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nv200_controller_widget.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QDoubleSpinBox,
    QFrame, QGridLayout, QSizePolicy, QSpacerItem,
    QSpinBox, QWidget)
import pysoworks_rc

class Ui_nv200ControllerWidget(object):
    def setupUi(self, nv200ControllerWidget):
        if not nv200ControllerWidget.objectName():
            nv200ControllerWidget.setObjectName(u"nv200ControllerWidget")
        nv200ControllerWidget.resize(1211, 738)
        nv200ControllerWidget.setAutoFillBackground(False)
        self.gridLayout = QGridLayout(nv200ControllerWidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.controllerStrcutureFrame = QFrame(nv200ControllerWidget)
        self.controllerStrcutureFrame.setObjectName(u"controllerStrcutureFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controllerStrcutureFrame.sizePolicy().hasHeightForWidth())
        self.controllerStrcutureFrame.setSizePolicy(sizePolicy)
        self.controllerStrcutureFrame.setMinimumSize(QSize(934, 479))
        self.controllerStrcutureFrame.setStyleSheet(u"#controllerStrcutureFrame{\n"
"background-image: url(:/assets/images/nv200_controller_structure.png) no-repeat left top;}\n"
"")
        self.pcfsEdit = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.pcfsEdit.setObjectName(u"pcfsEdit")
        self.pcfsEdit.setGeometry(QRect(509, 87, 135, 24))
        sizePolicy.setHeightForWidth(self.pcfsEdit.sizePolicy().hasHeightForWidth())
        self.pcfsEdit.setSizePolicy(sizePolicy)
        self.pcfsEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.pcfsEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.pcfsEdit.setDecimals(6)
        self.pcfaEdit = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.pcfaEdit.setObjectName(u"pcfaEdit")
        self.pcfaEdit.setGeometry(QRect(509, 25, 135, 24))
        sizePolicy.setHeightForWidth(self.pcfaEdit.sizePolicy().hasHeightForWidth())
        self.pcfaEdit.setSizePolicy(sizePolicy)
        self.pcfaEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.pcfaEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.pcfaEdit.setDecimals(6)
        self.doubleSpinBox_3 = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setGeometry(QRect(239, 175, 75, 24))
        sizePolicy.setHeightForWidth(self.doubleSpinBox_3.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_3.setSizePolicy(sizePolicy)
        self.doubleSpinBox_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBox_3.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBox_3.setDecimals(3)
        self.pcfvEdit = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.pcfvEdit.setObjectName(u"pcfvEdit")
        self.pcfvEdit.setGeometry(QRect(509, 51, 135, 24))
        sizePolicy.setHeightForWidth(self.pcfvEdit.sizePolicy().hasHeightForWidth())
        self.pcfvEdit.setSizePolicy(sizePolicy)
        self.pcfvEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.pcfvEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.pcfvEdit.setDecimals(6)
        self.doubleSpinBox = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setGeometry(QRect(87, 56, 104, 24))
        sizePolicy.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy)
        self.doubleSpinBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox_2 = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")
        self.doubleSpinBox_2.setGeometry(QRect(87, 87, 104, 24))
        sizePolicy.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy)
        self.doubleSpinBox_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.doubleSpinBox_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBox_2.setDecimals(3)
        self.pEdit = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.pEdit.setObjectName(u"pEdit")
        self.pEdit.setGeometry(QRect(522, 146, 120, 24))
        sizePolicy.setHeightForWidth(self.pEdit.sizePolicy().hasHeightForWidth())
        self.pEdit.setSizePolicy(sizePolicy)
        self.pEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.pEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.pEdit.setDecimals(3)
        self.iEdit = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.iEdit.setObjectName(u"iEdit")
        self.iEdit.setGeometry(QRect(522, 176, 120, 24))
        sizePolicy.setHeightForWidth(self.iEdit.sizePolicy().hasHeightForWidth())
        self.iEdit.setSizePolicy(sizePolicy)
        self.iEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.iEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.iEdit.setDecimals(3)
        self.dEdit = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.dEdit.setObjectName(u"dEdit")
        self.dEdit.setGeometry(QRect(522, 206, 120, 24))
        sizePolicy.setHeightForWidth(self.dEdit.sizePolicy().hasHeightForWidth())
        self.dEdit.setSizePolicy(sizePolicy)
        self.dEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.dEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.dEdit.setDecimals(3)
        self.spinBox = QSpinBox(self.controllerStrcutureFrame)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(347, 191, 94, 24))
        self.spinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.checkBox = QCheckBox(self.controllerStrcutureFrame)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(347, 162, 96, 20))
        self.checkBox.setProperty(u"toggleSwitch", True)
        self.checkBox_2 = QCheckBox(self.controllerStrcutureFrame)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(807, 161, 96, 20))
        self.checkBox_2.setProperty(u"toggleSwitch", True)
        self.spinBox_2 = QSpinBox(self.controllerStrcutureFrame)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setGeometry(QRect(807, 188, 118, 24))
        self.spinBox_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_3 = QSpinBox(self.controllerStrcutureFrame)
        self.spinBox_3.setObjectName(u"spinBox_3")
        self.spinBox_3.setGeometry(QRect(807, 218, 118, 24))
        self.spinBox_3.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.checkBox_3 = QCheckBox(self.controllerStrcutureFrame)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(237, 317, 105, 20))
        self.checkBox_3.setProperty(u"toggleSwitch", True)
        self.pEdit_2 = QDoubleSpinBox(self.controllerStrcutureFrame)
        self.pEdit_2.setObjectName(u"pEdit_2")
        self.pEdit_2.setGeometry(QRect(237, 344, 110, 24))
        sizePolicy.setHeightForWidth(self.pEdit_2.sizePolicy().hasHeightForWidth())
        self.pEdit_2.setSizePolicy(sizePolicy)
        self.pEdit_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.pEdit_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.pEdit_2.setDecimals(3)

        self.gridLayout.addWidget(self.controllerStrcutureFrame, 0, 0, 2, 2)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 0, 1, 2)


        self.retranslateUi(nv200ControllerWidget)

        QMetaObject.connectSlotsByName(nv200ControllerWidget)
    # setupUi

    def retranslateUi(self, nv200ControllerWidget):
        nv200ControllerWidget.setWindowTitle(QCoreApplication.translate("nv200ControllerWidget", u"Frame", None))
        self.pcfsEdit.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"pcf_s   ", None))
        self.pcfaEdit.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"pcf_a   ", None))
        self.doubleSpinBox_3.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"sr   ", None))
        self.pcfvEdit.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"pcv_v   ", None))
        self.doubleSpinBox.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"setst   ", None))
        self.doubleSpinBox_2.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"set   ", None))
        self.pEdit.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"P   ", None))
        self.iEdit.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"I   ", None))
        self.dEdit.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"D  ", None))
        self.spinBox.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"setlpf   ", None))
        self.checkBox.setText(QCoreApplication.translate("nv200ControllerWidget", u"setlpon", None))
        self.checkBox_2.setText(QCoreApplication.translate("nv200ControllerWidget", u"notchon", None))
        self.spinBox_2.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"notchf   ", None))
        self.spinBox_3.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"notchb   ", None))
        self.checkBox_3.setText(QCoreApplication.translate("nv200ControllerWidget", u"poslpon", None))
        self.pEdit_2.setPrefix(QCoreApplication.translate("nv200ControllerWidget", u"poslpf   ", None))
    # retranslateUi

