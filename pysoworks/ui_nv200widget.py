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
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

from mplcanvas import MplWidget
from timed_progress_bar import TimedProgressBar

class Ui_NV200Widget(object):
    def setupUi(self, NV200Widget):
        if not NV200Widget.objectName():
            NV200Widget.setObjectName(u"NV200Widget")
        NV200Widget.resize(1205, 821)
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
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.easyModeGroupBox = QGroupBox(NV200Widget)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.targetPosSpinBox.sizePolicy().hasHeightForWidth())
        self.targetPosSpinBox.setSizePolicy(sizePolicy2)
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
        sizePolicy2.setHeightForWidth(self.targetPosSpinBox_2.sizePolicy().hasHeightForWidth())
        self.targetPosSpinBox_2.setSizePolicy(sizePolicy2)
        self.targetPosSpinBox_2.setDecimals(3)
        self.targetPosSpinBox_2.setMaximum(1000.000000000000000)

        self.horizontalLayout_4.addWidget(self.targetPosSpinBox_2)

        self.moveButton_2 = QPushButton(self.easyModeGroupBox)
        self.moveButton_2.setObjectName(u"moveButton_2")
        sizePolicy1.setHeightForWidth(self.moveButton_2.sizePolicy().hasHeightForWidth())
        self.moveButton_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.moveButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addWidget(self.easyModeGroupBox)

        self.setpointParamGroupBox = QGroupBox(NV200Widget)
        self.setpointParamGroupBox.setObjectName(u"setpointParamGroupBox")
        self.verticalLayout_6 = QVBoxLayout(self.setpointParamGroupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.slewRateLabel = QLabel(self.setpointParamGroupBox)
        self.slewRateLabel.setObjectName(u"slewRateLabel")

        self.verticalLayout_6.addWidget(self.slewRateLabel)

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


        self.verticalLayout_2.addWidget(self.setpointParamGroupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.mplCanvasWidget = MplWidget(NV200Widget)
        self.mplCanvasWidget.setObjectName(u"mplCanvasWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.mplCanvasWidget.sizePolicy().hasHeightForWidth())
        self.mplCanvasWidget.setSizePolicy(sizePolicy3)

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
        self.setpointParamGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Setpoint Param.", None))
        self.slewRateLabel.setText(QCoreApplication.translate("NV200Widget", u"Slew Rate", None))
        self.setpointFilterCheckBox.setText(QCoreApplication.translate("NV200Widget", u"LP Filter Cutoff", None))
        self.setpointFilterCutoffSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" Hz", None))
    # retranslateUi

