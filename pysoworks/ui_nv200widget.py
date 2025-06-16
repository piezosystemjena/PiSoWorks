# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nv200widget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)

from pysoworks.mplcanvas import MplWidget
from pysoworks.timed_progress_bar import TimedProgressBar

class Ui_NV200Widget(object):
    def setupUi(self, NV200Widget):
        if not NV200Widget.objectName():
            NV200Widget.setObjectName(u"NV200Widget")
        NV200Widget.resize(1483, 1027)
        self.verticalLayout_3 = QVBoxLayout(NV200Widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.devicesComboBox = QComboBox(NV200Widget)
        self.devicesComboBox.setObjectName(u"devicesComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devicesComboBox.sizePolicy().hasHeightForWidth())
        self.devicesComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.devicesComboBox)

        self.searchDevicesButton = QPushButton(NV200Widget)
        self.searchDevicesButton.setObjectName(u"searchDevicesButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.searchDevicesButton.sizePolicy().hasHeightForWidth())
        self.searchDevicesButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.searchDevicesButton)

        self.connectButton = QPushButton(NV200Widget)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.connectButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.scrollArea = QScrollArea(NV200Widget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 188, 964))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.easyModeTab = QWidget()
        self.easyModeTab.setObjectName(u"easyModeTab")
        self.verticalLayout_7 = QVBoxLayout(self.easyModeTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.easyModeGroupBox = QGroupBox(self.easyModeTab)
        self.easyModeGroupBox.setObjectName(u"easyModeGroupBox")
        self.easyModeGroupBox.setEnabled(False)
        self.verticalLayout = QVBoxLayout(self.easyModeGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.openLoopButton = QRadioButton(self.easyModeGroupBox)
        self.openLoopButton.setObjectName(u"openLoopButton")
        self.openLoopButton.setChecked(True)

        self.verticalLayout.addWidget(self.openLoopButton)

        self.closedLoopButton = QRadioButton(self.easyModeGroupBox)
        self.closedLoopButton.setObjectName(u"closedLoopButton")

        self.verticalLayout.addWidget(self.closedLoopButton)

        self.label = QLabel(self.easyModeGroupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.targetPosSpinBox = QDoubleSpinBox(self.easyModeGroupBox)
        self.targetPosSpinBox.setObjectName(u"targetPosSpinBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.targetPosSpinBox.sizePolicy().hasHeightForWidth())
        self.targetPosSpinBox.setSizePolicy(sizePolicy3)
        self.targetPosSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.targetPosSpinBox.setDecimals(3)
        self.targetPosSpinBox.setMaximum(1000.000000000000000)

        self.horizontalLayout_3.addWidget(self.targetPosSpinBox)

        self.moveButton = QPushButton(self.easyModeGroupBox)
        self.moveButton.setObjectName(u"moveButton")
        sizePolicy1.setHeightForWidth(self.moveButton.sizePolicy().hasHeightForWidth())
        self.moveButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.moveButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, -1, -1)
        self.targetPosSpinBox_2 = QDoubleSpinBox(self.easyModeGroupBox)
        self.targetPosSpinBox_2.setObjectName(u"targetPosSpinBox_2")
        sizePolicy3.setHeightForWidth(self.targetPosSpinBox_2.sizePolicy().hasHeightForWidth())
        self.targetPosSpinBox_2.setSizePolicy(sizePolicy3)
        self.targetPosSpinBox_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.targetPosSpinBox_2.setDecimals(3)
        self.targetPosSpinBox_2.setMaximum(1000.000000000000000)

        self.horizontalLayout_4.addWidget(self.targetPosSpinBox_2)

        self.moveButton_2 = QPushButton(self.easyModeGroupBox)
        self.moveButton_2.setObjectName(u"moveButton_2")
        sizePolicy1.setHeightForWidth(self.moveButton_2.sizePolicy().hasHeightForWidth())
        self.moveButton_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.moveButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_7.addWidget(self.easyModeGroupBox)

        self.verticalSpacer = QSpacerItem(20, 740, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.easyModeTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.verticalLayout_8 = QVBoxLayout(self.settingsTab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.setpointParamGroupBox = QGroupBox(self.settingsTab)
        self.setpointParamGroupBox.setObjectName(u"setpointParamGroupBox")
        self.verticalLayout_6 = QVBoxLayout(self.setpointParamGroupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.slewRateLabel = QLabel(self.setpointParamGroupBox)
        self.slewRateLabel.setObjectName(u"slewRateLabel")

        self.horizontalLayout_5.addWidget(self.slewRateLabel, 0, Qt.AlignmentFlag.AlignBottom)

        self.applySetpointParamButton = QPushButton(self.setpointParamGroupBox)
        self.applySetpointParamButton.setObjectName(u"applySetpointParamButton")
        sizePolicy1.setHeightForWidth(self.applySetpointParamButton.sizePolicy().hasHeightForWidth())
        self.applySetpointParamButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.applySetpointParamButton, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.slewRateSpinBox = QDoubleSpinBox(self.setpointParamGroupBox)
        self.slewRateSpinBox.setObjectName(u"slewRateSpinBox")
        self.slewRateSpinBox.setDecimals(7)
        self.slewRateSpinBox.setMinimum(0.000000000000000)
        self.slewRateSpinBox.setMaximum(2000.000000000000000)
        self.slewRateSpinBox.setValue(0.000000000000000)

        self.verticalLayout_6.addWidget(self.slewRateSpinBox)

        self.setpointFilterCheckBox = QCheckBox(self.setpointParamGroupBox)
        self.setpointFilterCheckBox.setObjectName(u"setpointFilterCheckBox")

        self.verticalLayout_6.addWidget(self.setpointFilterCheckBox)

        self.setpointFilterCutoffSpinBox = QSpinBox(self.setpointParamGroupBox)
        self.setpointFilterCutoffSpinBox.setObjectName(u"setpointFilterCutoffSpinBox")
        self.setpointFilterCutoffSpinBox.setMinimum(1)
        self.setpointFilterCutoffSpinBox.setMaximum(10000)

        self.verticalLayout_6.addWidget(self.setpointFilterCutoffSpinBox)


        self.verticalLayout_8.addWidget(self.setpointParamGroupBox)

        self.settingsGroupBox = QGroupBox(self.settingsTab)
        self.settingsGroupBox.setObjectName(u"settingsGroupBox")
        self.settingsGroupBox.setMinimumSize(QSize(0, 100))
        self.verticalLayout_5 = QVBoxLayout(self.settingsGroupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.label_2 = QLabel(self.settingsGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.modsrcComboBox = QComboBox(self.settingsGroupBox)
        self.modsrcComboBox.setObjectName(u"modsrcComboBox")

        self.verticalLayout_5.addWidget(self.modsrcComboBox)

        self.label_3 = QLabel(self.settingsGroupBox)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_5.addWidget(self.label_3)

        self.spisrcComboBox = QComboBox(self.settingsGroupBox)
        self.spisrcComboBox.setObjectName(u"spisrcComboBox")

        self.verticalLayout_5.addWidget(self.spisrcComboBox)


        self.verticalLayout_8.addWidget(self.settingsGroupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 654, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.settingsTab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_2.addWidget(self.scrollArea)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.mplCanvasWidget = MplWidget(NV200Widget)
        self.mplCanvasWidget.setObjectName(u"mplCanvasWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.mplCanvasWidget.sizePolicy().hasHeightForWidth())
        self.mplCanvasWidget.setSizePolicy(sizePolicy4)

        self.verticalLayout_4.addWidget(self.mplCanvasWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.moveProgressBar = TimedProgressBar(NV200Widget)
        self.moveProgressBar.setObjectName(u"moveProgressBar")
        self.moveProgressBar.setMaximumSize(QSize(16777215, 5))
        self.moveProgressBar.setValue(0)
        self.moveProgressBar.setTextVisible(False)

        self.verticalLayout_3.addWidget(self.moveProgressBar)


        self.retranslateUi(NV200Widget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(NV200Widget)
    # setupUi

    def retranslateUi(self, NV200Widget):
        NV200Widget.setWindowTitle(QCoreApplication.translate("NV200Widget", u"Form", None))
        self.searchDevicesButton.setText(QCoreApplication.translate("NV200Widget", u"Search Devices ...", None))
        self.connectButton.setText(QCoreApplication.translate("NV200Widget", u"Connect", None))
        self.easyModeGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Easy Mode", None))
        self.openLoopButton.setText(QCoreApplication.translate("NV200Widget", u"Open Loop", None))
        self.closedLoopButton.setText(QCoreApplication.translate("NV200Widget", u"Closed Loop", None))
        self.label.setText(QCoreApplication.translate("NV200Widget", u"Target Positions", None))
        self.moveButton.setText("")
        self.moveButton_2.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.easyModeTab), QCoreApplication.translate("NV200Widget", u"Easy Mode", None))
        self.setpointParamGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Setpoint Param.", None))
        self.slewRateLabel.setText(QCoreApplication.translate("NV200Widget", u"Slew Rate", None))
        self.applySetpointParamButton.setText(QCoreApplication.translate("NV200Widget", u"Apply", None))
        self.setpointFilterCheckBox.setText(QCoreApplication.translate("NV200Widget", u"LP Filter", None))
        self.setpointFilterCutoffSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" Hz", None))
        self.settingsGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Settings", None))
        self.label_2.setText(QCoreApplication.translate("NV200Widget", u"Setpoint Source:", None))
#if QT_CONFIG(tooltip)
        self.modsrcComboBox.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p>Signal source for setppoint (modsrc)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("NV200Widget", u"SPI-Monitor Source:", None))
#if QT_CONFIG(tooltip)
        self.spisrcComboBox.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p>SPI monitor/ Return value via MISO (spisrc)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("NV200Widget", u"Settings", None))
    # retranslateUi

