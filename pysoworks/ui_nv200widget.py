# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nv200widget.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDoubleSpinBox, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QSplitter, QStackedWidget, QTabWidget,
    QToolButton, QVBoxLayout, QWidget)

from pysoworks.consolewidget import Console
from pysoworks.data_recorder_widget import DataRecorderWidget
from pysoworks.mplcanvas import MplWidget
from pysoworks.nv200_controller_widget import Nv200ControllerWidget
from pysoworks.timed_progress_bar import TimedProgressBar

class Ui_NV200Widget(object):
    def setupUi(self, NV200Widget):
        if not NV200Widget.objectName():
            NV200Widget.setObjectName(u"NV200Widget")
        NV200Widget.resize(1462, 1147)
        self.verticalLayout_3 = QVBoxLayout(NV200Widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(9, -1, -1, -1)
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

        self.searchDevicesButton = QToolButton(NV200Widget)
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

        self.connectButton = QPushButton(NV200Widget)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy1)
        self.connectButton.setProperty(u"alignedWithEdit", True)

        self.horizontalLayout.addWidget(self.connectButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.splitter = QSplitter(NV200Widget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, -1, -1, -1)
        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setMinimumSize(QSize(0, 10))
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 266, 668))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy3)
        self.scrollAreaWidgetContents.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy4)
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.West)
        self.easyModeTab = QWidget()
        self.easyModeTab.setObjectName(u"easyModeTab")
        self.verticalLayout_7 = QVBoxLayout(self.easyModeTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.easyModeGroupBox = QGroupBox(self.easyModeTab)
        self.easyModeGroupBox.setObjectName(u"easyModeGroupBox")
        self.easyModeGroupBox.setEnabled(False)
        self.verticalLayout = QVBoxLayout(self.easyModeGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.closedLoopCheckBox = QCheckBox(self.easyModeGroupBox)
        self.closedLoopCheckBox.setObjectName(u"closedLoopCheckBox")
        self.closedLoopCheckBox.setProperty(u"toggleSwitch", True)

        self.verticalLayout.addWidget(self.closedLoopCheckBox)

        self.verticalSpacer_3 = QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.targetPositionsLabel = QLabel(self.easyModeGroupBox)
        self.targetPositionsLabel.setObjectName(u"targetPositionsLabel")

        self.verticalLayout.addWidget(self.targetPositionsLabel)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.targetPosSpinBox_2 = QDoubleSpinBox(self.easyModeGroupBox)
        self.targetPosSpinBox_2.setObjectName(u"targetPosSpinBox_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.targetPosSpinBox_2.sizePolicy().hasHeightForWidth())
        self.targetPosSpinBox_2.setSizePolicy(sizePolicy5)
        self.targetPosSpinBox_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.targetPosSpinBox_2.setDecimals(3)
        self.targetPosSpinBox_2.setMaximum(1000.000000000000000)

        self.gridLayout.addWidget(self.targetPosSpinBox_2, 1, 0, 1, 1)

        self.moveButton_2 = QPushButton(self.easyModeGroupBox)
        self.moveButton_2.setObjectName(u"moveButton_2")
        sizePolicy1.setHeightForWidth(self.moveButton_2.sizePolicy().hasHeightForWidth())
        self.moveButton_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.moveButton_2, 1, 1, 1, 1)

        self.targetPosSpinBox = QDoubleSpinBox(self.easyModeGroupBox)
        self.targetPosSpinBox.setObjectName(u"targetPosSpinBox")
        sizePolicy5.setHeightForWidth(self.targetPosSpinBox.sizePolicy().hasHeightForWidth())
        self.targetPosSpinBox.setSizePolicy(sizePolicy5)
        self.targetPosSpinBox.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.targetPosSpinBox.setDecimals(3)
        self.targetPosSpinBox.setMaximum(1000.000000000000000)

        self.gridLayout.addWidget(self.targetPosSpinBox, 0, 0, 1, 1)

        self.moveButton = QPushButton(self.easyModeGroupBox)
        self.moveButton.setObjectName(u"moveButton")
        sizePolicy1.setHeightForWidth(self.moveButton.sizePolicy().hasHeightForWidth())
        self.moveButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.moveButton, 0, 1, 1, 1)

        self.rangeLabel = QLabel(self.easyModeGroupBox)
        self.rangeLabel.setObjectName(u"rangeLabel")
        self.rangeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.rangeLabel, 2, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.verticalLayout_7.addWidget(self.easyModeGroupBox)

        self.verticalSpacer = QSpacerItem(20, 740, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.easyModeTab, "")
        self.settingsTab = QWidget()
        self.settingsTab.setObjectName(u"settingsTab")
        self.verticalLayout_8 = QVBoxLayout(self.settingsTab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.applyButton = QPushButton(self.settingsTab)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.applyButton)

        self.retrieveButton = QPushButton(self.settingsTab)
        self.retrieveButton.setObjectName(u"retrieveButton")

        self.verticalLayout_8.addWidget(self.retrieveButton)

        self.verticalSpacer_10 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_10)

        self.restorePrevButton = QPushButton(self.settingsTab)
        self.restorePrevButton.setObjectName(u"restorePrevButton")

        self.verticalLayout_8.addWidget(self.restorePrevButton)

        self.restoreInitialButton = QPushButton(self.settingsTab)
        self.restoreInitialButton.setObjectName(u"restoreInitialButton")

        self.verticalLayout_8.addWidget(self.restoreInitialButton)

        self.restoreDefaultButton = QPushButton(self.settingsTab)
        self.restoreDefaultButton.setObjectName(u"restoreDefaultButton")

        self.verticalLayout_8.addWidget(self.restoreDefaultButton)

        self.verticalSpacer_11 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_11)

        self.exportSettingsButton = QPushButton(self.settingsTab)
        self.exportSettingsButton.setObjectName(u"exportSettingsButton")

        self.verticalLayout_8.addWidget(self.exportSettingsButton)

        self.loadSettingsButton = QPushButton(self.settingsTab)
        self.loadSettingsButton.setObjectName(u"loadSettingsButton")

        self.verticalLayout_8.addWidget(self.loadSettingsButton)

        self.verticalSpacer_2 = QSpacerItem(20, 654, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.settingsTab, "")
        self.waveformTab = QWidget()
        self.waveformTab.setObjectName(u"waveformTab")
        self.verticalLayout_4 = QVBoxLayout(self.waveformTab)
        self.verticalLayout_4.setSpacing(12)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.waveformGroupBox = QGroupBox(self.waveformTab)
        self.waveformGroupBox.setObjectName(u"waveformGroupBox")
        self.formLayout = QFormLayout(self.waveformGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.wavefomLabel = QLabel(self.waveformGroupBox)
        self.wavefomLabel.setObjectName(u"wavefomLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.wavefomLabel)

        self.waveFormComboBox = QComboBox(self.waveformGroupBox)
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.setObjectName(u"waveFormComboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.waveFormComboBox)

        self.verticalSpacer_6 = QSpacerItem(167, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout.setItem(1, QFormLayout.ItemRole.SpanningRole, self.verticalSpacer_6)

        self.freqLabel = QLabel(self.waveformGroupBox)
        self.freqLabel.setObjectName(u"freqLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.freqLabel)

        self.freqSpinBox = QDoubleSpinBox(self.waveformGroupBox)
        self.freqSpinBox.setObjectName(u"freqSpinBox")
        sizePolicy5.setHeightForWidth(self.freqSpinBox.sizePolicy().hasHeightForWidth())
        self.freqSpinBox.setSizePolicy(sizePolicy5)
        self.freqSpinBox.setMinimum(0.010000000000000)
        self.freqSpinBox.setMaximum(100000.000000000000000)
        self.freqSpinBox.setValue(20.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.freqSpinBox)

        self.waveSamplingPeriodLabel = QLabel(self.waveformGroupBox)
        self.waveSamplingPeriodLabel.setObjectName(u"waveSamplingPeriodLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.waveSamplingPeriodLabel)

        self.waveSamplingPeriodSpinBox = QDoubleSpinBox(self.waveformGroupBox)
        self.waveSamplingPeriodSpinBox.setObjectName(u"waveSamplingPeriodSpinBox")
        self.waveSamplingPeriodSpinBox.setReadOnly(False)
        self.waveSamplingPeriodSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.waveSamplingPeriodSpinBox.setMaximum(3276.800000000000182)
        self.waveSamplingPeriodSpinBox.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.waveSamplingPeriodSpinBox)

        self.phaseLabel = QLabel(self.waveformGroupBox)
        self.phaseLabel.setObjectName(u"phaseLabel")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.phaseLabel)

        self.phaseShiftSpinBox = QDoubleSpinBox(self.waveformGroupBox)
        self.phaseShiftSpinBox.setObjectName(u"phaseShiftSpinBox")
        sizePolicy5.setHeightForWidth(self.phaseShiftSpinBox.sizePolicy().hasHeightForWidth())
        self.phaseShiftSpinBox.setSizePolicy(sizePolicy5)
        self.phaseShiftSpinBox.setDecimals(3)
        self.phaseShiftSpinBox.setMinimum(0.000000000000000)
        self.phaseShiftSpinBox.setMaximum(360.000000000000000)
        self.phaseShiftSpinBox.setValue(0.000000000000000)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.phaseShiftSpinBox)

        self.dutyCycleLabel = QLabel(self.waveformGroupBox)
        self.dutyCycleLabel.setObjectName(u"dutyCycleLabel")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.dutyCycleLabel)

        self.dutyCycleSpinBox = QDoubleSpinBox(self.waveformGroupBox)
        self.dutyCycleSpinBox.setObjectName(u"dutyCycleSpinBox")
        self.dutyCycleSpinBox.setDecimals(1)
        self.dutyCycleSpinBox.setMinimum(0.100000000000000)
        self.dutyCycleSpinBox.setValue(50.000000000000000)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.dutyCycleSpinBox)

        self.verticalSpacer_5 = QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout.setItem(7, QFormLayout.ItemRole.FieldRole, self.verticalSpacer_5)

        self.highLabel = QLabel(self.waveformGroupBox)
        self.highLabel.setObjectName(u"highLabel")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.highLabel)

        self.highLevelSpinBox = QDoubleSpinBox(self.waveformGroupBox)
        self.highLevelSpinBox.setObjectName(u"highLevelSpinBox")
        sizePolicy5.setHeightForWidth(self.highLevelSpinBox.sizePolicy().hasHeightForWidth())
        self.highLevelSpinBox.setSizePolicy(sizePolicy5)
        self.highLevelSpinBox.setDecimals(3)
        self.highLevelSpinBox.setMaximum(1000.000000000000000)

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.highLevelSpinBox)

        self.lowLabel = QLabel(self.waveformGroupBox)
        self.lowLabel.setObjectName(u"lowLabel")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.lowLabel)

        self.lowLevelSpinBox = QDoubleSpinBox(self.waveformGroupBox)
        self.lowLevelSpinBox.setObjectName(u"lowLevelSpinBox")
        sizePolicy5.setHeightForWidth(self.lowLevelSpinBox.sizePolicy().hasHeightForWidth())
        self.lowLevelSpinBox.setSizePolicy(sizePolicy5)
        self.lowLevelSpinBox.setDecimals(3)
        self.lowLevelSpinBox.setMaximum(1000.000000000000000)

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.lowLevelSpinBox)

        self.uploadButton = QPushButton(self.waveformGroupBox)
        self.uploadButton.setObjectName(u"uploadButton")
        sizePolicy5.setHeightForWidth(self.uploadButton.sizePolicy().hasHeightForWidth())
        self.uploadButton.setSizePolicy(sizePolicy5)
        self.uploadButton.setCheckable(True)

        self.formLayout.setWidget(12, QFormLayout.ItemRole.SpanningRole, self.uploadButton)

        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout.setItem(11, QFormLayout.ItemRole.LabelRole, self.verticalSpacer_4)

        self.customLabel = QLabel(self.waveformGroupBox)
        self.customLabel.setObjectName(u"customLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.customLabel)

        self.importButton = QPushButton(self.waveformGroupBox)
        self.importButton.setObjectName(u"importButton")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.importButton)


        self.verticalLayout_4.addWidget(self.waveformGroupBox)

        self.generatorGroupBox = QGroupBox(self.waveformTab)
        self.generatorGroupBox.setObjectName(u"generatorGroupBox")
        self.formLayout_2 = QFormLayout(self.generatorGroupBox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.cyclesSpinBox = QSpinBox(self.generatorGroupBox)
        self.cyclesSpinBox.setObjectName(u"cyclesSpinBox")
        sizePolicy5.setHeightForWidth(self.cyclesSpinBox.sizePolicy().hasHeightForWidth())
        self.cyclesSpinBox.setSizePolicy(sizePolicy5)
        self.cyclesSpinBox.setMaximum(65535)
        self.cyclesSpinBox.setValue(1)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cyclesSpinBox)

        self.cyclesLabel = QLabel(self.generatorGroupBox)
        self.cyclesLabel.setObjectName(u"cyclesLabel")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.cyclesLabel)

        self.totalDurationLabel = QLabel(self.generatorGroupBox)
        self.totalDurationLabel.setObjectName(u"totalDurationLabel")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.totalDurationLabel)

        self.waveformDurationSpinBox = QSpinBox(self.generatorGroupBox)
        self.waveformDurationSpinBox.setObjectName(u"waveformDurationSpinBox")
        self.waveformDurationSpinBox.setReadOnly(True)
        self.waveformDurationSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.waveformDurationSpinBox.setMaximum(16777215)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.waveformDurationSpinBox)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.startWaveformButton = QPushButton(self.generatorGroupBox)
        self.startWaveformButton.setObjectName(u"startWaveformButton")
        sizePolicy5.setHeightForWidth(self.startWaveformButton.sizePolicy().hasHeightForWidth())
        self.startWaveformButton.setSizePolicy(sizePolicy5)

        self.horizontalLayout_6.addWidget(self.startWaveformButton)

        self.stopWaveformButton = QPushButton(self.generatorGroupBox)
        self.stopWaveformButton.setObjectName(u"stopWaveformButton")
        sizePolicy5.setHeightForWidth(self.stopWaveformButton.sizePolicy().hasHeightForWidth())
        self.stopWaveformButton.setSizePolicy(sizePolicy5)

        self.horizontalLayout_6.addWidget(self.stopWaveformButton)


        self.formLayout_2.setLayout(4, QFormLayout.ItemRole.SpanningRole, self.horizontalLayout_6)

        self.recSyncCheckBox = QCheckBox(self.generatorGroupBox)
        self.recSyncCheckBox.setObjectName(u"recSyncCheckBox")
        self.recSyncCheckBox.setChecked(True)
        self.recSyncCheckBox.setProperty(u"toggleSwitch", True)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.recSyncCheckBox)

        self.recSyncLabel = QLabel(self.generatorGroupBox)
        self.recSyncLabel.setObjectName(u"recSyncLabel")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.recSyncLabel)

        self.verticalSpacer_8 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout_2.setItem(3, QFormLayout.ItemRole.LabelRole, self.verticalSpacer_8)


        self.verticalLayout_4.addWidget(self.generatorGroupBox)

        self.hysteresisGroupBox = QGroupBox(self.waveformTab)
        self.hysteresisGroupBox.setObjectName(u"hysteresisGroupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.hysteresisGroupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.measureHysteresisButton = QPushButton(self.hysteresisGroupBox)
        self.measureHysteresisButton.setObjectName(u"measureHysteresisButton")

        self.horizontalLayout_3.addWidget(self.measureHysteresisButton)

        self.plotHysteresisButton = QPushButton(self.hysteresisGroupBox)
        self.plotHysteresisButton.setObjectName(u"plotHysteresisButton")

        self.horizontalLayout_3.addWidget(self.plotHysteresisButton)


        self.verticalLayout_4.addWidget(self.hysteresisGroupBox)

        self.verticalSpacer_7 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_7)

        self.tabWidget.addTab(self.waveformTab, "")
        self.resonanceTab = QWidget()
        self.resonanceTab.setObjectName(u"resonanceTab")
        self.verticalLayout_6 = QVBoxLayout(self.resonanceTab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.resonanceButton = QPushButton(self.resonanceTab)
        self.resonanceButton.setObjectName(u"resonanceButton")

        self.verticalLayout_6.addWidget(self.resonanceButton)

        self.impulseVoltagesGroupBox = QGroupBox(self.resonanceTab)
        self.impulseVoltagesGroupBox.setObjectName(u"impulseVoltagesGroupBox")
        self.formLayout_3 = QFormLayout(self.impulseVoltagesGroupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.impulsePeakVoltageLabel = QLabel(self.impulseVoltagesGroupBox)
        self.impulsePeakVoltageLabel.setObjectName(u"impulsePeakVoltageLabel")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.impulsePeakVoltageLabel)

        self.impulsePeakVoltageSpinBox = QDoubleSpinBox(self.impulseVoltagesGroupBox)
        self.impulsePeakVoltageSpinBox.setObjectName(u"impulsePeakVoltageSpinBox")
        self.impulsePeakVoltageSpinBox.setReadOnly(True)
        self.impulsePeakVoltageSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.impulsePeakVoltageSpinBox.setDecimals(1)
        self.impulsePeakVoltageSpinBox.setMinimum(-10000.000000000000000)
        self.impulsePeakVoltageSpinBox.setMaximum(10000.000000000000000)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.impulsePeakVoltageSpinBox)

        self.impulseBaseVoltageLabel = QLabel(self.impulseVoltagesGroupBox)
        self.impulseBaseVoltageLabel.setObjectName(u"impulseBaseVoltageLabel")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.impulseBaseVoltageLabel)

        self.impulseBaseVoltageSpinBox = QDoubleSpinBox(self.impulseVoltagesGroupBox)
        self.impulseBaseVoltageSpinBox.setObjectName(u"impulseBaseVoltageSpinBox")
        self.impulseBaseVoltageSpinBox.setReadOnly(True)
        self.impulseBaseVoltageSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.impulseBaseVoltageSpinBox.setDecimals(1)
        self.impulseBaseVoltageSpinBox.setMinimum(-10000.000000000000000)
        self.impulseBaseVoltageSpinBox.setMaximum(10000.000000000000000)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.impulseBaseVoltageSpinBox)


        self.verticalLayout_6.addWidget(self.impulseVoltagesGroupBox)

        self.verticalSpacer_9 = QSpacerItem(10, 626, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_9)

        self.tabWidget.addTab(self.resonanceTab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_10.addWidget(self.scrollArea)

        self.piezoIconLabel = QLabel(self.layoutWidget)
        self.piezoIconLabel.setObjectName(u"piezoIconLabel")
        sizePolicy5.setHeightForWidth(self.piezoIconLabel.sizePolicy().hasHeightForWidth())
        self.piezoIconLabel.setSizePolicy(sizePolicy5)
        self.piezoIconLabel.setStyleSheet(u"QLabel {margin-top: 12px; margin-left: 4px;}")

        self.verticalLayout_10.addWidget(self.piezoIconLabel)

        self.consoleButton = QToolButton(self.layoutWidget)
        self.consoleButton.setObjectName(u"consoleButton")
        sizePolicy1.setHeightForWidth(self.consoleButton.sizePolicy().hasHeightForWidth())
        self.consoleButton.setSizePolicy(sizePolicy1)
        self.consoleButton.setAutoRaise(True)

        self.verticalLayout_10.addWidget(self.consoleButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout_10)

        self.stackedWidget = QStackedWidget(self.layoutWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy6)
        self.easyModePlot = MplWidget()
        self.easyModePlot.setObjectName(u"easyModePlot")
        self.stackedWidget.addWidget(self.easyModePlot)
        self.controllerStructureWidget = Nv200ControllerWidget()
        self.controllerStructureWidget.setObjectName(u"controllerStructureWidget")
        self.stackedWidget.addWidget(self.controllerStructureWidget)
        self.waveformPlots = QWidget()
        self.waveformPlots.setObjectName(u"waveformPlots")
        self.verticalLayout_9 = QVBoxLayout(self.waveformPlots)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.splitter_2 = QSplitter(self.waveformPlots)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.waveformPlot = DataRecorderWidget(self.splitter_2)
        self.waveformPlot.setObjectName(u"waveformPlot")
        self.splitter_2.addWidget(self.waveformPlot)
        self.hysteresisPlot = MplWidget(self.splitter_2)
        self.hysteresisPlot.setObjectName(u"hysteresisPlot")
        self.splitter_2.addWidget(self.hysteresisPlot)

        self.verticalLayout_9.addWidget(self.splitter_2)

        self.stackedWidget.addWidget(self.waveformPlots)
        self.resonancePlots = QWidget()
        self.resonancePlots.setObjectName(u"resonancePlots")
        self.verticalLayout_5 = QVBoxLayout(self.resonancePlots)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.impulsePlot = MplWidget(self.resonancePlots)
        self.impulsePlot.setObjectName(u"impulsePlot")

        self.verticalLayout_5.addWidget(self.impulsePlot)

        self.resonancePlot = MplWidget(self.resonancePlots)
        self.resonancePlot.setObjectName(u"resonancePlot")

        self.verticalLayout_5.addWidget(self.resonancePlot)

        self.stackedWidget.addWidget(self.resonancePlots)

        self.horizontalLayout_2.addWidget(self.stackedWidget)

        self.splitter.addWidget(self.layoutWidget)
        self.consoleWidget = QWidget(self.splitter)
        self.consoleWidget.setObjectName(u"consoleWidget")
        sizePolicy6.setHeightForWidth(self.consoleWidget.sizePolicy().hasHeightForWidth())
        self.consoleWidget.setSizePolicy(sizePolicy6)
        self.consoleWidget.setMinimumSize(QSize(0, 0))
        self.verticalLayout_11 = QVBoxLayout(self.consoleWidget)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.consoleLabel = QLabel(self.consoleWidget)
        self.consoleLabel.setObjectName(u"consoleLabel")
        sizePolicy5.setHeightForWidth(self.consoleLabel.sizePolicy().hasHeightForWidth())
        self.consoleLabel.setSizePolicy(sizePolicy5)

        self.verticalLayout_11.addWidget(self.consoleLabel)

        self.console = Console(self.consoleWidget)
        self.console.setObjectName(u"console")
        sizePolicy6.setHeightForWidth(self.console.sizePolicy().hasHeightForWidth())
        self.console.setSizePolicy(sizePolicy6)
        self.console.setStyleSheet(u"QTextEdit { background: black; }")

        self.verticalLayout_11.addWidget(self.console)

        self.splitter.addWidget(self.consoleWidget)

        self.verticalLayout_3.addWidget(self.splitter)

        self.mainProgressBar = TimedProgressBar(NV200Widget)
        self.mainProgressBar.setObjectName(u"mainProgressBar")
        self.mainProgressBar.setMaximumSize(QSize(16777215, 3))
        self.mainProgressBar.setStyleSheet(u"QProgressBar { background: transparent;}")
        self.mainProgressBar.setValue(0)
        self.mainProgressBar.setTextVisible(False)

        self.verticalLayout_3.addWidget(self.mainProgressBar)


        self.retranslateUi(NV200Widget)

        self.tabWidget.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(NV200Widget)
    # setupUi

    def retranslateUi(self, NV200Widget):
        NV200Widget.setWindowTitle(QCoreApplication.translate("NV200Widget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.devicesComboBox.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Device List</span></p><p>List of detected NV200 devices.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.searchDevicesButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Search Devices</span></p><p>Search for all NV200 devices connected via USB or Ethernet. Click the menu button to search only USB or only Ethernet devices.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.searchDevicesButton.setText(QCoreApplication.translate("NV200Widget", u"Search Devices ...", None))
        self.searchDevicesButton.setProperty(u"style", QCoreApplication.translate("NV200Widget", u"pushButton", None))
#if QT_CONFIG(tooltip)
        self.connectButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Connect</span></p><p>Connect to the device you selected from the list.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.connectButton.setText(QCoreApplication.translate("NV200Widget", u"Connect", None))
        self.easyModeGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Easy Mode", None))
#if QT_CONFIG(tooltip)
        self.closedLoopCheckBox.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Open Loop / Closed Loop</span></p><p>Toggles between open loop (OL) and closed loop (CL) mode. In open loop mode the PID-controller is bridged and the command input directly controls the amplifier. The resulting piezo stroke then depends on the characteristic of the piezo actuator and is affected by piezo-typical creeping and hysteresis behavior.</p><p>In closed loop mode (CL), these effects will be compensated by the digital loop controller.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.closedLoopCheckBox.setText(QCoreApplication.translate("NV200Widget", u"Open Loop", None))
        self.targetPositionsLabel.setText(QCoreApplication.translate("NV200Widget", u"Setpoints", None))
#if QT_CONFIG(tooltip)
        self.targetPosSpinBox_2.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Setpoint 2</span></p><p>The second setpoint. Depending on the Open Loop / Closed Loop switch this value is given as voltage (Open Loop) or as position in \u00b5m or mrad (Closed Loop).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.moveButton_2.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Move To Setpoint 2</span></p><p>Starts the move to 2nd setpoint.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.moveButton_2.setText("")
#if QT_CONFIG(tooltip)
        self.targetPosSpinBox.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Setpoint 1</span></p><p>The first setpoint. Depending on the Open Loop / Closed Loop switch this value is given as voltage (Open Loop) or as position in \u00b5m or mrad (Closed Loop).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.targetPosSpinBox.setPrefix("")
        self.targetPosSpinBox.setSuffix("")
#if QT_CONFIG(tooltip)
        self.moveButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Move To Setpoint 1 </span></p><p>Starts the move to first setpoint.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.moveButton.setText("")
        self.rangeLabel.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.easyModeTab), QCoreApplication.translate("NV200Widget", u"Easy Mode", None))
#if QT_CONFIG(tooltip)
        self.applyButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Apply Parameters</span></p><p>Send the currently edited parameters to the device to update its configuration.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.applyButton.setText(QCoreApplication.translate("NV200Widget", u"Apply Parameters", None))
        self.applyButton.setProperty(u"text-align", QCoreApplication.translate("NV200Widget", u"left", None))
#if QT_CONFIG(tooltip)
        self.retrieveButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Retrieve Parameters</span></p><p>Read the current parameters from the device and update the local view in case you modified the parameters from outside or via a terminal program.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.retrieveButton.setText(QCoreApplication.translate("NV200Widget", u"Retrieve Parameters", None))
        self.retrieveButton.setProperty(u"text-align", QCoreApplication.translate("NV200Widget", u"left", None))
#if QT_CONFIG(tooltip)
        self.restorePrevButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Restore Previous Parameters</span></p><p>Reverts parameters to their values before the last time you clicked &quot;Apply Parameters&quot;.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.restorePrevButton.setText(QCoreApplication.translate("NV200Widget", u"Restore Previous Parameters", None))
        self.restorePrevButton.setProperty(u"text-align", QCoreApplication.translate("NV200Widget", u"left", None))
#if QT_CONFIG(tooltip)
        self.restoreInitialButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Restore Initial Parameters</span></p><p>Load the parameters as they were when the device was first connected this session.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.restoreInitialButton.setText(QCoreApplication.translate("NV200Widget", u"Restore Initial Parameters", None))
        self.restoreInitialButton.setProperty(u"text-align", QCoreApplication.translate("NV200Widget", u"left", None))
#if QT_CONFIG(tooltip)
        self.restoreDefaultButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Restore Original Parameters</span></p><p>Restore the parameters that were backed up when this device was first connected.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.restoreDefaultButton.setText(QCoreApplication.translate("NV200Widget", u"Restore Original Parameters", None))
        self.restoreDefaultButton.setProperty(u"text-align", QCoreApplication.translate("NV200Widget", u"left", None))
#if QT_CONFIG(tooltip)
        self.exportSettingsButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Export Parameters</span></p><p>Exports the current parameters into a parameters *.ini file.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.exportSettingsButton.setText(QCoreApplication.translate("NV200Widget", u"Export Parameters", None))
        self.exportSettingsButton.setProperty(u"text-align", QCoreApplication.translate("NV200Widget", u"left", None))
#if QT_CONFIG(tooltip)
        self.loadSettingsButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Load Parameters</span></p><p>Loads the parameters from a previously exported *.ini file.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.loadSettingsButton.setText(QCoreApplication.translate("NV200Widget", u"Load Parameters", None))
        self.loadSettingsButton.setProperty(u"text-align", QCoreApplication.translate("NV200Widget", u"left", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("NV200Widget", u"Settings", None))
        self.waveformGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Waveform Settings", None))
        self.wavefomLabel.setText(QCoreApplication.translate("NV200Widget", u"Waveform", None))
        self.waveFormComboBox.setItemText(0, QCoreApplication.translate("NV200Widget", u"Sine", None))
        self.waveFormComboBox.setItemText(1, QCoreApplication.translate("NV200Widget", u"Triangle", None))
        self.waveFormComboBox.setItemText(2, QCoreApplication.translate("NV200Widget", u"Square", None))
        self.waveFormComboBox.setItemText(3, QCoreApplication.translate("NV200Widget", u"Custom", None))

        self.freqLabel.setText(QCoreApplication.translate("NV200Widget", u"Freq.", None))
        self.freqSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" Hz", None))
        self.waveSamplingPeriodLabel.setText(QCoreApplication.translate("NV200Widget", u"Sampling Period", None))
        self.waveSamplingPeriodSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" ms", None))
        self.phaseLabel.setText(QCoreApplication.translate("NV200Widget", u"Phase Shift", None))
        self.phaseShiftSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" \u00b0", None))
        self.dutyCycleLabel.setText(QCoreApplication.translate("NV200Widget", u"Duty Cycle", None))
        self.dutyCycleSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" %", None))
        self.highLabel.setText(QCoreApplication.translate("NV200Widget", u"High Level", None))
        self.lowLabel.setText(QCoreApplication.translate("NV200Widget", u"Low Level", None))
        self.uploadButton.setText(QCoreApplication.translate("NV200Widget", u"Upload", None))
        self.customLabel.setText(QCoreApplication.translate("NV200Widget", u"Cust. Waveform", None))
        self.importButton.setText(QCoreApplication.translate("NV200Widget", u"Load CSV / Excel", None))
        self.generatorGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Generator Control", None))
        self.cyclesLabel.setText(QCoreApplication.translate("NV200Widget", u"Cycles", None))
        self.totalDurationLabel.setText(QCoreApplication.translate("NV200Widget", u"Total Duration", None))
        self.waveformDurationSpinBox.setSpecialValueText(QCoreApplication.translate("NV200Widget", u"infinite", None))
        self.waveformDurationSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" ms", None))
        self.startWaveformButton.setText(QCoreApplication.translate("NV200Widget", u"Start", None))
        self.stopWaveformButton.setText(QCoreApplication.translate("NV200Widget", u"Stop", None))
        self.recSyncCheckBox.setText("")
        self.recSyncLabel.setText(QCoreApplication.translate("NV200Widget", u"Sync Rec. Duration", None))
        self.hysteresisGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Hysteresis Measurement", None))
        self.measureHysteresisButton.setText(QCoreApplication.translate("NV200Widget", u"Measure", None))
        self.plotHysteresisButton.setText(QCoreApplication.translate("NV200Widget", u"Plot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.waveformTab), QCoreApplication.translate("NV200Widget", u"Waveform", None))
        self.resonanceButton.setText(QCoreApplication.translate("NV200Widget", u"Get Resonance Spectrum", None))
        self.impulseVoltagesGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Impulse Voltages", None))
        self.impulsePeakVoltageLabel.setText(QCoreApplication.translate("NV200Widget", u"Peak Voltage:", None))
        self.impulsePeakVoltageSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" V", None))
        self.impulseBaseVoltageLabel.setText(QCoreApplication.translate("NV200Widget", u"Base Voltage:", None))
        self.impulseBaseVoltageSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" V", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resonanceTab), QCoreApplication.translate("NV200Widget", u"Impulse Response", None))
        self.piezoIconLabel.setText(QCoreApplication.translate("NV200Widget", u"piezosystemjena Icon", None))
#if QT_CONFIG(tooltip)
        self.consoleButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Show / Hide Command Console</span></p><p>Toggle the command console display.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.consoleButton.setText(QCoreApplication.translate("NV200Widget", u"Console", None))
        self.consoleLabel.setText(QCoreApplication.translate("NV200Widget", u"Command Line Interface", None))
#if QT_CONFIG(tooltip)
        self.console.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Command Console</span></p><p>Enter NV200 commands or help to show all commands</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

