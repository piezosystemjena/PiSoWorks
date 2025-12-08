# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spiboxwidget.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QToolButton, QVBoxLayout, QWidget)

from pisoworks.mplcanvas import MplWidget
from pisoworks.timed_progress_bar import TimedProgressBar
from pisoworks.waveform_options_widget import WaveformOptionsWidget

class Ui_SpiBoxWidget(object):
    def setupUi(self, SpiBoxWidget):
        if not SpiBoxWidget.objectName():
            SpiBoxWidget.setObjectName(u"SpiBoxWidget")
        SpiBoxWidget.resize(847, 642)
        self.verticalLayout_3 = QVBoxLayout(SpiBoxWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.devicesComboBox = QComboBox(SpiBoxWidget)
        self.devicesComboBox.setObjectName(u"devicesComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devicesComboBox.sizePolicy().hasHeightForWidth())
        self.devicesComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.devicesComboBox)

        self.searchDevicesButton = QToolButton(SpiBoxWidget)
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

        self.connectButton = QPushButton(SpiBoxWidget)
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
        self.singleDatasetGroupBox = QGroupBox(SpiBoxWidget)
        self.singleDatasetGroupBox.setObjectName(u"singleDatasetGroupBox")
        self.singleDatasetGroupBox.setEnabled(True)
        self.singleDatasetGroupBox.setMinimumSize(QSize(0, 0))
        self.gridLayout = QGridLayout(self.singleDatasetGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.singleDatasetSendCh1SpinBox = QDoubleSpinBox(self.singleDatasetGroupBox)
        self.singleDatasetSendCh1SpinBox.setObjectName(u"singleDatasetSendCh1SpinBox")
        self.singleDatasetSendCh1SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.singleDatasetSendCh1SpinBox.setDecimals(3)
        self.singleDatasetSendCh1SpinBox.setMaximum(100.000000000000000)
        self.singleDatasetSendCh1SpinBox.setSingleStep(10.000000000000000)

        self.gridLayout.addWidget(self.singleDatasetSendCh1SpinBox, 1, 1, 1, 1)

        self.singleDatasetReceiveCh1SpinBox = QDoubleSpinBox(self.singleDatasetGroupBox)
        self.singleDatasetReceiveCh1SpinBox.setObjectName(u"singleDatasetReceiveCh1SpinBox")
        self.singleDatasetReceiveCh1SpinBox.setReadOnly(True)
        self.singleDatasetReceiveCh1SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.singleDatasetReceiveCh1SpinBox.setDecimals(3)
        self.singleDatasetReceiveCh1SpinBox.setMaximum(1000.000000000000000)

        self.gridLayout.addWidget(self.singleDatasetReceiveCh1SpinBox, 1, 3, 1, 1)

        self.label_3 = QLabel(self.singleDatasetGroupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.label_4 = QLabel(self.singleDatasetGroupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)

        self.label = QLabel(self.singleDatasetGroupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_2 = QLabel(self.singleDatasetGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.singleDatasetReceiveCh3SpinBox = QDoubleSpinBox(self.singleDatasetGroupBox)
        self.singleDatasetReceiveCh3SpinBox.setObjectName(u"singleDatasetReceiveCh3SpinBox")
        self.singleDatasetReceiveCh3SpinBox.setReadOnly(True)
        self.singleDatasetReceiveCh3SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.singleDatasetReceiveCh3SpinBox.setDecimals(3)
        self.singleDatasetReceiveCh3SpinBox.setMaximum(1000.000000000000000)

        self.gridLayout.addWidget(self.singleDatasetReceiveCh3SpinBox, 3, 3, 1, 1)

        self.singleDatasetReceiveCh2SpinBox = QDoubleSpinBox(self.singleDatasetGroupBox)
        self.singleDatasetReceiveCh2SpinBox.setObjectName(u"singleDatasetReceiveCh2SpinBox")
        self.singleDatasetReceiveCh2SpinBox.setReadOnly(True)
        self.singleDatasetReceiveCh2SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.singleDatasetReceiveCh2SpinBox.setDecimals(3)
        self.singleDatasetReceiveCh2SpinBox.setMaximum(1000.000000000000000)

        self.gridLayout.addWidget(self.singleDatasetReceiveCh2SpinBox, 2, 3, 1, 1)

        self.singleDatasetSendCh3SpinBox = QDoubleSpinBox(self.singleDatasetGroupBox)
        self.singleDatasetSendCh3SpinBox.setObjectName(u"singleDatasetSendCh3SpinBox")
        self.singleDatasetSendCh3SpinBox.setReadOnly(False)
        self.singleDatasetSendCh3SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.singleDatasetSendCh3SpinBox.setDecimals(3)
        self.singleDatasetSendCh3SpinBox.setMaximum(100.000000000000000)
        self.singleDatasetSendCh3SpinBox.setSingleStep(10.000000000000000)

        self.gridLayout.addWidget(self.singleDatasetSendCh3SpinBox, 3, 1, 1, 1)

        self.label_5 = QLabel(self.singleDatasetGroupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.sendSingleButton = QPushButton(self.singleDatasetGroupBox)
        self.sendSingleButton.setObjectName(u"sendSingleButton")

        self.gridLayout.addWidget(self.sendSingleButton, 4, 1, 1, 3)

        self.line = QFrame(self.singleDatasetGroupBox)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 0))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 1, 2, 3, 1)

        self.singleDatasetSendCh2SpinBox = QDoubleSpinBox(self.singleDatasetGroupBox)
        self.singleDatasetSendCh2SpinBox.setObjectName(u"singleDatasetSendCh2SpinBox")
        self.singleDatasetSendCh2SpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.singleDatasetSendCh2SpinBox.setDecimals(3)
        self.singleDatasetSendCh2SpinBox.setMaximum(100.000000000000000)
        self.singleDatasetSendCh2SpinBox.setSingleStep(10.000000000000000)

        self.gridLayout.addWidget(self.singleDatasetSendCh2SpinBox, 2, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.singleDatasetGroupBox)

        self.multipleDatasetGroupBox = QGroupBox(SpiBoxWidget)
        self.multipleDatasetGroupBox.setObjectName(u"multipleDatasetGroupBox")
        self.multipleDatasetGroupBox.setEnabled(True)
        self.multipleDatasetGroupBox.setMinimumSize(QSize(0, 0))
        self.multipleGridLayout = QGridLayout(self.multipleDatasetGroupBox)
        self.multipleGridLayout.setObjectName(u"multipleGridLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.startWaveformButton = QPushButton(self.multipleDatasetGroupBox)
        self.startWaveformButton.setObjectName(u"startWaveformButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.startWaveformButton.sizePolicy().hasHeightForWidth())
        self.startWaveformButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.startWaveformButton)

        self.getResponseButton = QPushButton(self.multipleDatasetGroupBox)
        self.getResponseButton.setObjectName(u"getResponseButton")
        self.getResponseButton.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.getResponseButton.sizePolicy().hasHeightForWidth())
        self.getResponseButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.getResponseButton)


        self.multipleGridLayout.addLayout(self.horizontalLayout_4, 5, 0, 1, 1)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.infiniteCyclesLabel = QLabel(self.multipleDatasetGroupBox)
        self.infiniteCyclesLabel.setObjectName(u"infiniteCyclesLabel")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.infiniteCyclesLabel)

        self.infiniteCyclesCheckBox = QCheckBox(self.multipleDatasetGroupBox)
        self.infiniteCyclesCheckBox.setObjectName(u"infiniteCyclesCheckBox")
        self.infiniteCyclesCheckBox.setProperty(u"toggleSwitch", True)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.infiniteCyclesCheckBox)

        self.cyclesLabel = QLabel(self.multipleDatasetGroupBox)
        self.cyclesLabel.setObjectName(u"cyclesLabel")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.cyclesLabel)

        self.cyclesSpinBox = QSpinBox(self.multipleDatasetGroupBox)
        self.cyclesSpinBox.setObjectName(u"cyclesSpinBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cyclesSpinBox.sizePolicy().hasHeightForWidth())
        self.cyclesSpinBox.setSizePolicy(sizePolicy3)
        self.cyclesSpinBox.setMinimum(1)
        self.cyclesSpinBox.setMaximum(65535)
        self.cyclesSpinBox.setValue(1)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cyclesSpinBox)


        self.multipleGridLayout.addLayout(self.formLayout_2, 2, 0, 1, 1)

        self.channelTabWidget = QTabWidget(self.multipleDatasetGroupBox)
        self.channelTabWidget.setObjectName(u"channelTabWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.channelTabWidget.sizePolicy().hasHeightForWidth())
        self.channelTabWidget.setSizePolicy(sizePolicy4)
        self.channel1Tab = QWidget()
        self.channel1Tab.setObjectName(u"channel1Tab")
        sizePolicy4.setHeightForWidth(self.channel1Tab.sizePolicy().hasHeightForWidth())
        self.channel1Tab.setSizePolicy(sizePolicy4)
        self.channel1Tab.setAcceptDrops(False)
        self.vBoxLayout1 = QVBoxLayout(self.channel1Tab)
        self.vBoxLayout1.setObjectName(u"vBoxLayout1")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setContentsMargins(9, 6, 6, 0)
        self.enabledLabel1 = QLabel(self.channel1Tab)
        self.enabledLabel1.setObjectName(u"enabledLabel1")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.enabledLabel1.sizePolicy().hasHeightForWidth())
        self.enabledLabel1.setSizePolicy(sizePolicy5)
        self.enabledLabel1.setBaseSize(QSize(0, 0))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.enabledLabel1)

        self.enabledCheckbox1 = QCheckBox(self.channel1Tab)
        self.enabledCheckbox1.setObjectName(u"enabledCheckbox1")
        self.enabledCheckbox1.setChecked(False)
        self.enabledCheckbox1.setProperty(u"toggleSwitch", True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.enabledCheckbox1)


        self.vBoxLayout1.addLayout(self.formLayout)

        self.waveformOptions1 = WaveformOptionsWidget(self.channel1Tab)
        self.waveformOptions1.setObjectName(u"waveformOptions1")

        self.vBoxLayout1.addWidget(self.waveformOptions1)

        self.channelTabWidget.addTab(self.channel1Tab, "")
        self.channel2Tab = QWidget()
        self.channel2Tab.setObjectName(u"channel2Tab")
        sizePolicy4.setHeightForWidth(self.channel2Tab.sizePolicy().hasHeightForWidth())
        self.channel2Tab.setSizePolicy(sizePolicy4)
        self.formLayout2 = QVBoxLayout(self.channel2Tab)
        self.formLayout2.setObjectName(u"formLayout2")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(9, 6, 6, -1)
        self.enabledLabel2 = QLabel(self.channel2Tab)
        self.enabledLabel2.setObjectName(u"enabledLabel2")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.enabledLabel2)

        self.enabledCheckbox2 = QCheckBox(self.channel2Tab)
        self.enabledCheckbox2.setObjectName(u"enabledCheckbox2")
        self.enabledCheckbox2.setChecked(False)
        self.enabledCheckbox2.setProperty(u"toggleSwitch", True)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.enabledCheckbox2)


        self.formLayout2.addLayout(self.formLayout_3)

        self.waveformOptions2 = WaveformOptionsWidget(self.channel2Tab)
        self.waveformOptions2.setObjectName(u"waveformOptions2")

        self.formLayout2.addWidget(self.waveformOptions2)

        self.channelTabWidget.addTab(self.channel2Tab, "")
        self.channel3Tab = QWidget()
        self.channel3Tab.setObjectName(u"channel3Tab")
        sizePolicy4.setHeightForWidth(self.channel3Tab.sizePolicy().hasHeightForWidth())
        self.channel3Tab.setSizePolicy(sizePolicy4)
        self.formLayout3 = QVBoxLayout(self.channel3Tab)
        self.formLayout3.setObjectName(u"formLayout3")
        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setContentsMargins(9, 6, 6, -1)
        self.enabledLabel3 = QLabel(self.channel3Tab)
        self.enabledLabel3.setObjectName(u"enabledLabel3")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.enabledLabel3)

        self.enabledCheckbox3 = QCheckBox(self.channel3Tab)
        self.enabledCheckbox3.setObjectName(u"enabledCheckbox3")
        self.enabledCheckbox3.setChecked(False)
        self.enabledCheckbox3.setProperty(u"toggleSwitch", True)

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.enabledCheckbox3)


        self.formLayout3.addLayout(self.formLayout_4)

        self.waveformOptions3 = WaveformOptionsWidget(self.channel3Tab)
        self.waveformOptions3.setObjectName(u"waveformOptions3")

        self.formLayout3.addWidget(self.waveformOptions3)

        self.channelTabWidget.addTab(self.channel3Tab, "")

        self.multipleGridLayout.addWidget(self.channelTabWidget, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.multipleDatasetGroupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.waveformPlot = MplWidget(SpiBoxWidget)
        self.waveformPlot.setObjectName(u"waveformPlot")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.waveformPlot.sizePolicy().hasHeightForWidth())
        self.waveformPlot.setSizePolicy(sizePolicy6)

        self.verticalLayout_4.addWidget(self.waveformPlot)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.moveProgressBar = TimedProgressBar(SpiBoxWidget)
        self.moveProgressBar.setObjectName(u"moveProgressBar")
        self.moveProgressBar.setMaximumSize(QSize(16777215, 3))
        self.moveProgressBar.setStyleSheet(u"QProgressBar { background: transparent;}")
        self.moveProgressBar.setValue(0)
        self.moveProgressBar.setTextVisible(False)

        self.verticalLayout_3.addWidget(self.moveProgressBar)


        self.retranslateUi(SpiBoxWidget)

        self.channelTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SpiBoxWidget)
    # setupUi

    def retranslateUi(self, SpiBoxWidget):
        SpiBoxWidget.setWindowTitle(QCoreApplication.translate("SpiBoxWidget", u"Form", None))
        self.searchDevicesButton.setText(QCoreApplication.translate("SpiBoxWidget", u"Search Devices ...", None))
        self.searchDevicesButton.setProperty(u"style", QCoreApplication.translate("SpiBoxWidget", u"pushButton", None))
        self.connectButton.setText(QCoreApplication.translate("SpiBoxWidget", u"Connect", None))
        self.singleDatasetGroupBox.setTitle(QCoreApplication.translate("SpiBoxWidget", u"Single Dataset", None))
        self.singleDatasetSendCh1SpinBox.setSuffix(QCoreApplication.translate("SpiBoxWidget", u" %", None))
        self.singleDatasetReceiveCh1SpinBox.setSuffix(QCoreApplication.translate("SpiBoxWidget", u" %", None))
        self.label_3.setText(QCoreApplication.translate("SpiBoxWidget", u"Send", None))
        self.label_4.setText(QCoreApplication.translate("SpiBoxWidget", u"Receive", None))
        self.label.setText(QCoreApplication.translate("SpiBoxWidget", u"Channel 1:", None))
        self.label_2.setText(QCoreApplication.translate("SpiBoxWidget", u"Channel 2:", None))
        self.singleDatasetReceiveCh3SpinBox.setSuffix(QCoreApplication.translate("SpiBoxWidget", u" %", None))
        self.singleDatasetReceiveCh2SpinBox.setSuffix(QCoreApplication.translate("SpiBoxWidget", u" %", None))
        self.singleDatasetSendCh3SpinBox.setSuffix(QCoreApplication.translate("SpiBoxWidget", u" %", None))
        self.label_5.setText(QCoreApplication.translate("SpiBoxWidget", u"Channel 3:", None))
        self.sendSingleButton.setText(QCoreApplication.translate("SpiBoxWidget", u"Send", None))
        self.singleDatasetSendCh2SpinBox.setSuffix(QCoreApplication.translate("SpiBoxWidget", u" %", None))
        self.multipleDatasetGroupBox.setTitle(QCoreApplication.translate("SpiBoxWidget", u"Multiple Datasets", None))
        self.startWaveformButton.setText(QCoreApplication.translate("SpiBoxWidget", u"Start", None))
        self.getResponseButton.setText(QCoreApplication.translate("SpiBoxWidget", u"Plot Data", None))
        self.infiniteCyclesLabel.setText(QCoreApplication.translate("SpiBoxWidget", u"Infinite Cycles", None))
        self.infiniteCyclesCheckBox.setText("")
        self.cyclesLabel.setText(QCoreApplication.translate("SpiBoxWidget", u"Cycles", None))
        self.enabledLabel1.setText(QCoreApplication.translate("SpiBoxWidget", u"Enabled              ", None))
        self.enabledCheckbox1.setText("")
        self.channelTabWidget.setTabText(self.channelTabWidget.indexOf(self.channel1Tab), QCoreApplication.translate("SpiBoxWidget", u"Channel 1", None))
        self.enabledLabel2.setText(QCoreApplication.translate("SpiBoxWidget", u"Enabled              ", None))
        self.enabledCheckbox2.setText("")
        self.channelTabWidget.setTabText(self.channelTabWidget.indexOf(self.channel2Tab), QCoreApplication.translate("SpiBoxWidget", u"Channel 2", None))
        self.enabledLabel3.setText(QCoreApplication.translate("SpiBoxWidget", u"Enabled              ", None))
        self.enabledCheckbox3.setText("")
        self.channelTabWidget.setTabText(self.channelTabWidget.indexOf(self.channel3Tab), QCoreApplication.translate("SpiBoxWidget", u"Channel 3", None))
    # retranslateUi

