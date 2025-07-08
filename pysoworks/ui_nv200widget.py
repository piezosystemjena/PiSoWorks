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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QSplitter, QStackedWidget, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)

from pysoworks.consolewidget import Console
from pysoworks.mplcanvas import MplWidget
from pysoworks.nv200_controller_widget import Nv200ControllerWidget
from pysoworks.timed_progress_bar import TimedProgressBar

class Ui_NV200Widget(object):
    def setupUi(self, NV200Widget):
        if not NV200Widget.objectName():
            NV200Widget.setObjectName(u"NV200Widget")
        NV200Widget.resize(1376, 994)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 247, 582))
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy3)
        self.scrollAreaWidgetContents.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 30, 0)
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

        self.verticalLayout_8.addWidget(self.applyButton)

        self.retrieveButton = QPushButton(self.settingsTab)
        self.retrieveButton.setObjectName(u"retrieveButton")

        self.verticalLayout_8.addWidget(self.retrieveButton)

        self.restoreButton = QPushButton(self.settingsTab)
        self.restoreButton.setObjectName(u"restoreButton")

        self.verticalLayout_8.addWidget(self.restoreButton)

        self.verticalSpacer_2 = QSpacerItem(20, 654, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.settingsTab, "")
        self.waveformTab = QWidget()
        self.waveformTab.setObjectName(u"waveformTab")
        self.formLayout = QFormLayout(self.waveformTab)
        self.formLayout.setObjectName(u"formLayout")
        self.freqLabel = QLabel(self.waveformTab)
        self.freqLabel.setObjectName(u"freqLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.freqLabel)

        self.freqSpinBox = QDoubleSpinBox(self.waveformTab)
        self.freqSpinBox.setObjectName(u"freqSpinBox")
        sizePolicy5.setHeightForWidth(self.freqSpinBox.sizePolicy().hasHeightForWidth())
        self.freqSpinBox.setSizePolicy(sizePolicy5)
        self.freqSpinBox.setMinimum(0.010000000000000)
        self.freqSpinBox.setMaximum(100.000000000000000)
        self.freqSpinBox.setValue(20.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.freqSpinBox)

        self.phaseLabel = QLabel(self.waveformTab)
        self.phaseLabel.setObjectName(u"phaseLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.phaseLabel)

        self.phaseShiftSpinBox = QDoubleSpinBox(self.waveformTab)
        self.phaseShiftSpinBox.setObjectName(u"phaseShiftSpinBox")
        sizePolicy5.setHeightForWidth(self.phaseShiftSpinBox.sizePolicy().hasHeightForWidth())
        self.phaseShiftSpinBox.setSizePolicy(sizePolicy5)
        self.phaseShiftSpinBox.setDecimals(3)
        self.phaseShiftSpinBox.setMinimum(0.000000000000000)
        self.phaseShiftSpinBox.setMaximum(360.000000000000000)
        self.phaseShiftSpinBox.setValue(0.000000000000000)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.phaseShiftSpinBox)

        self.highLabel = QLabel(self.waveformTab)
        self.highLabel.setObjectName(u"highLabel")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.highLabel)

        self.highLevelSpinBox = QDoubleSpinBox(self.waveformTab)
        self.highLevelSpinBox.setObjectName(u"highLevelSpinBox")
        sizePolicy5.setHeightForWidth(self.highLevelSpinBox.sizePolicy().hasHeightForWidth())
        self.highLevelSpinBox.setSizePolicy(sizePolicy5)
        self.highLevelSpinBox.setDecimals(3)
        self.highLevelSpinBox.setMaximum(1000.000000000000000)

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.highLevelSpinBox)

        self.lowLabel = QLabel(self.waveformTab)
        self.lowLabel.setObjectName(u"lowLabel")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.lowLabel)

        self.lowLevelSpinBox = QDoubleSpinBox(self.waveformTab)
        self.lowLevelSpinBox.setObjectName(u"lowLevelSpinBox")
        sizePolicy5.setHeightForWidth(self.lowLevelSpinBox.sizePolicy().hasHeightForWidth())
        self.lowLevelSpinBox.setSizePolicy(sizePolicy5)
        self.lowLevelSpinBox.setDecimals(3)
        self.lowLevelSpinBox.setMaximum(1000.000000000000000)

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.lowLevelSpinBox)

        self.uploadButton = QPushButton(self.waveformTab)
        self.uploadButton.setObjectName(u"uploadButton")
        sizePolicy5.setHeightForWidth(self.uploadButton.sizePolicy().hasHeightForWidth())
        self.uploadButton.setSizePolicy(sizePolicy5)

        self.formLayout.setWidget(9, QFormLayout.ItemRole.SpanningRole, self.uploadButton)

        self.verticalSpacer_4 = QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout.setItem(10, QFormLayout.ItemRole.FieldRole, self.verticalSpacer_4)

        self.cyclesLabel = QLabel(self.waveformTab)
        self.cyclesLabel.setObjectName(u"cyclesLabel")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.cyclesLabel)

        self.cyclesSpinBox = QSpinBox(self.waveformTab)
        self.cyclesSpinBox.setObjectName(u"cyclesSpinBox")
        sizePolicy5.setHeightForWidth(self.cyclesSpinBox.sizePolicy().hasHeightForWidth())
        self.cyclesSpinBox.setSizePolicy(sizePolicy5)
        self.cyclesSpinBox.setMaximum(65535)
        self.cyclesSpinBox.setValue(1)

        self.formLayout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.cyclesSpinBox)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.startWaveformButton = QPushButton(self.waveformTab)
        self.startWaveformButton.setObjectName(u"startWaveformButton")
        sizePolicy5.setHeightForWidth(self.startWaveformButton.sizePolicy().hasHeightForWidth())
        self.startWaveformButton.setSizePolicy(sizePolicy5)

        self.horizontalLayout_6.addWidget(self.startWaveformButton)

        self.stopWaveformButton = QPushButton(self.waveformTab)
        self.stopWaveformButton.setObjectName(u"stopWaveformButton")
        sizePolicy5.setHeightForWidth(self.stopWaveformButton.sizePolicy().hasHeightForWidth())
        self.stopWaveformButton.setSizePolicy(sizePolicy5)

        self.horizontalLayout_6.addWidget(self.stopWaveformButton)


        self.formLayout.setLayout(12, QFormLayout.ItemRole.SpanningRole, self.horizontalLayout_6)

        self.dutyCycleLabel = QLabel(self.waveformTab)
        self.dutyCycleLabel.setObjectName(u"dutyCycleLabel")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.dutyCycleLabel)

        self.dutyCycleSpinBox = QDoubleSpinBox(self.waveformTab)
        self.dutyCycleSpinBox.setObjectName(u"dutyCycleSpinBox")
        self.dutyCycleSpinBox.setDecimals(1)
        self.dutyCycleSpinBox.setMinimum(0.100000000000000)
        self.dutyCycleSpinBox.setValue(50.000000000000000)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.dutyCycleSpinBox)

        self.verticalSpacer_5 = QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout.setItem(6, QFormLayout.ItemRole.FieldRole, self.verticalSpacer_5)

        self.waveFormComboBox = QComboBox(self.waveformTab)
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.setObjectName(u"waveFormComboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.waveFormComboBox)

        self.wavefomLabel = QLabel(self.waveformTab)
        self.wavefomLabel.setObjectName(u"wavefomLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.wavefomLabel)

        self.verticalSpacer_6 = QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout.setItem(1, QFormLayout.ItemRole.SpanningRole, self.verticalSpacer_6)

        self.tabWidget.addTab(self.waveformTab, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_10.addWidget(self.scrollArea)

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
        self.mplCanvasWidget = MplWidget()
        self.mplCanvasWidget.setObjectName(u"mplCanvasWidget")
        self.stackedWidget.addWidget(self.mplCanvasWidget)
        self.controllerStructureWidget = Nv200ControllerWidget()
        self.controllerStructureWidget.setObjectName(u"controllerStructureWidget")
        self.stackedWidget.addWidget(self.controllerStructureWidget)

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

        self.moveProgressBar = TimedProgressBar(NV200Widget)
        self.moveProgressBar.setObjectName(u"moveProgressBar")
        self.moveProgressBar.setMaximumSize(QSize(16777215, 3))
        self.moveProgressBar.setStyleSheet(u"QProgressBar { background: transparent;}")
        self.moveProgressBar.setValue(0)
        self.moveProgressBar.setTextVisible(False)

        self.verticalLayout_3.addWidget(self.moveProgressBar)


        self.retranslateUi(NV200Widget)

        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(NV200Widget)
    # setupUi

    def retranslateUi(self, NV200Widget):
        NV200Widget.setWindowTitle(QCoreApplication.translate("NV200Widget", u"Form", None))
        self.searchDevicesButton.setText(QCoreApplication.translate("NV200Widget", u"Search Devices ...", None))
        self.searchDevicesButton.setProperty(u"style", QCoreApplication.translate("NV200Widget", u"pushButton", None))
        self.connectButton.setText(QCoreApplication.translate("NV200Widget", u"Connect", None))
        self.easyModeGroupBox.setTitle(QCoreApplication.translate("NV200Widget", u"Easy Mode", None))
        self.closedLoopCheckBox.setText(QCoreApplication.translate("NV200Widget", u"Open Loop", None))
        self.targetPositionsLabel.setText(QCoreApplication.translate("NV200Widget", u"Target Positions:", None))
        self.moveButton_2.setText("")
        self.targetPosSpinBox.setPrefix("")
        self.targetPosSpinBox.setSuffix("")
        self.moveButton.setText("")
        self.rangeLabel.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.easyModeTab), QCoreApplication.translate("NV200Widget", u"Easy Mode", None))
#if QT_CONFIG(tooltip)
        self.applyButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Apply Parameters</span></p><p>Send the currently edited parameters to the device to update its configuration.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.applyButton.setText(QCoreApplication.translate("NV200Widget", u"Apply Parameters", None))
#if QT_CONFIG(tooltip)
        self.retrieveButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Retrieve Parameters</span></p><p>Read the current parameters from the device and update the local view.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.retrieveButton.setText(QCoreApplication.translate("NV200Widget", u"Retrieve Parameters", None))
#if QT_CONFIG(tooltip)
        self.restoreButton.setToolTip(QCoreApplication.translate("NV200Widget", u"<html><head/><body><p><span style=\" font-weight:700;\">Restore Default Parameters</span></p><p>Reset the device parameters to their previous values.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.restoreButton.setText(QCoreApplication.translate("NV200Widget", u"Restore Default Parameters", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), QCoreApplication.translate("NV200Widget", u"Settings", None))
        self.freqLabel.setText(QCoreApplication.translate("NV200Widget", u"Freq.", None))
        self.freqSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" Hz", None))
        self.phaseLabel.setText(QCoreApplication.translate("NV200Widget", u"Phase Shift", None))
        self.phaseShiftSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" \u00b0", None))
        self.highLabel.setText(QCoreApplication.translate("NV200Widget", u"High Level", None))
        self.lowLabel.setText(QCoreApplication.translate("NV200Widget", u"Low Level", None))
        self.uploadButton.setText(QCoreApplication.translate("NV200Widget", u"Upload", None))
        self.cyclesLabel.setText(QCoreApplication.translate("NV200Widget", u"Cycles", None))
        self.startWaveformButton.setText(QCoreApplication.translate("NV200Widget", u"Start", None))
        self.stopWaveformButton.setText(QCoreApplication.translate("NV200Widget", u"Stop", None))
        self.dutyCycleLabel.setText(QCoreApplication.translate("NV200Widget", u"Duty Cycle", None))
        self.dutyCycleSpinBox.setSuffix(QCoreApplication.translate("NV200Widget", u" %", None))
        self.waveFormComboBox.setItemText(0, QCoreApplication.translate("NV200Widget", u"Sine", None))
        self.waveFormComboBox.setItemText(1, QCoreApplication.translate("NV200Widget", u"Triangle", None))
        self.waveFormComboBox.setItemText(2, QCoreApplication.translate("NV200Widget", u"Square", None))

        self.wavefomLabel.setText(QCoreApplication.translate("NV200Widget", u"Waveform", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.waveformTab), QCoreApplication.translate("NV200Widget", u"Waveform", None))
        self.consoleButton.setText(QCoreApplication.translate("NV200Widget", u"Console", None))
        self.consoleLabel.setText(QCoreApplication.translate("NV200Widget", u"Command Line Interface", None))
    # retranslateUi

