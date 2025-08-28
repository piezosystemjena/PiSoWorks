# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spiboxwidget.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

from pysoworks.mplcanvas import MplWidget
from pysoworks.timed_progress_bar import TimedProgressBar

class Ui_SpiBoxWidget(object):
    def setupUi(self, SpiBoxWidget):
        if not SpiBoxWidget.objectName():
            SpiBoxWidget.setObjectName(u"SpiBoxWidget")
        SpiBoxWidget.resize(1205, 821)
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

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.waveformPlot = MplWidget(SpiBoxWidget)
        self.waveformPlot.setObjectName(u"waveformPlot")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.waveformPlot.sizePolicy().hasHeightForWidth())
        self.waveformPlot.setSizePolicy(sizePolicy2)

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
    # retranslateUi

