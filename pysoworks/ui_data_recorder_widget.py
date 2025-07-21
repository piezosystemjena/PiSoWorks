# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_recorder_widget.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

from pysoworks.mplcanvas import MplWidget

class Ui_DataRecorderWidget(object):
    def setupUi(self, DataRecorderWidget):
        if not DataRecorderWidget.objectName():
            DataRecorderWidget.setObjectName(u"DataRecorderWidget")
        DataRecorderWidget.resize(1109, 767)
        self.verticalLayout = QVBoxLayout(DataRecorderWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.dataRecSettingsGroupBox = QGroupBox(DataRecorderWidget)
        self.dataRecSettingsGroupBox.setObjectName(u"dataRecSettingsGroupBox")
        self.horizontalLayout = QHBoxLayout(self.dataRecSettingsGroupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.channel1Label = QLabel(self.dataRecSettingsGroupBox)
        self.channel1Label.setObjectName(u"channel1Label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.channel1Label.sizePolicy().hasHeightForWidth())
        self.channel1Label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.channel1Label)

        self.recsrc1ComboBox = QComboBox(self.dataRecSettingsGroupBox)
        self.recsrc1ComboBox.setObjectName(u"recsrc1ComboBox")

        self.horizontalLayout.addWidget(self.recsrc1ComboBox)

        self.channekl2Label = QLabel(self.dataRecSettingsGroupBox)
        self.channekl2Label.setObjectName(u"channekl2Label")
        sizePolicy.setHeightForWidth(self.channekl2Label.sizePolicy().hasHeightForWidth())
        self.channekl2Label.setSizePolicy(sizePolicy)
        self.channekl2Label.setStyleSheet(u"margin-left: 6px")

        self.horizontalLayout.addWidget(self.channekl2Label)

        self.recsrc2ComboBox = QComboBox(self.dataRecSettingsGroupBox)
        self.recsrc2ComboBox.setObjectName(u"recsrc2ComboBox")

        self.horizontalLayout.addWidget(self.recsrc2ComboBox)

        self.recDurationLabel = QLabel(self.dataRecSettingsGroupBox)
        self.recDurationLabel.setObjectName(u"recDurationLabel")
        self.recDurationLabel.setStyleSheet(u"margin-left: 6px")

        self.horizontalLayout.addWidget(self.recDurationLabel)

        self.recDurationSpinBox = QSpinBox(self.dataRecSettingsGroupBox)
        self.recDurationSpinBox.setObjectName(u"recDurationSpinBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.recDurationSpinBox.sizePolicy().hasHeightForWidth())
        self.recDurationSpinBox.setSizePolicy(sizePolicy1)
        self.recDurationSpinBox.setMinimum(1)
        self.recDurationSpinBox.setMaximum(5000)

        self.horizontalLayout.addWidget(self.recDurationSpinBox)

        self.samplingPeriodLabel = QLabel(self.dataRecSettingsGroupBox)
        self.samplingPeriodLabel.setObjectName(u"samplingPeriodLabel")
        self.samplingPeriodLabel.setStyleSheet(u"margin-left: 6px")

        self.horizontalLayout.addWidget(self.samplingPeriodLabel)

        self.samplePeriodSpinBox = QDoubleSpinBox(self.dataRecSettingsGroupBox)
        self.samplePeriodSpinBox.setObjectName(u"samplePeriodSpinBox")
        sizePolicy1.setHeightForWidth(self.samplePeriodSpinBox.sizePolicy().hasHeightForWidth())
        self.samplePeriodSpinBox.setSizePolicy(sizePolicy1)
        self.samplePeriodSpinBox.setReadOnly(True)
        self.samplePeriodSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.samplePeriodSpinBox.setMaximum(16777215.000000000000000)

        self.horizontalLayout.addWidget(self.samplePeriodSpinBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.historyLabel = QLabel(self.dataRecSettingsGroupBox)
        self.historyLabel.setObjectName(u"historyLabel")

        self.horizontalLayout.addWidget(self.historyLabel)

        self.historyCheckBox = QCheckBox(self.dataRecSettingsGroupBox)
        self.historyCheckBox.setObjectName(u"historyCheckBox")
        self.historyCheckBox.setChecked(False)
        self.historyCheckBox.setProperty(u"toggleSwitch", True)

        self.horizontalLayout.addWidget(self.historyCheckBox)

        self.clearPlotButton = QPushButton(self.dataRecSettingsGroupBox)
        self.clearPlotButton.setObjectName(u"clearPlotButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.clearPlotButton.sizePolicy().hasHeightForWidth())
        self.clearPlotButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.clearPlotButton)


        self.verticalLayout.addWidget(self.dataRecSettingsGroupBox)

        self.mplWidget = MplWidget(DataRecorderWidget)
        self.mplWidget.setObjectName(u"mplWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.mplWidget.sizePolicy().hasHeightForWidth())
        self.mplWidget.setSizePolicy(sizePolicy3)
        self.mplWidget.setStyleSheet(u"background: lightgrey")

        self.verticalLayout.addWidget(self.mplWidget)


        self.retranslateUi(DataRecorderWidget)

        QMetaObject.connectSlotsByName(DataRecorderWidget)
    # setupUi

    def retranslateUi(self, DataRecorderWidget):
        DataRecorderWidget.setWindowTitle(QCoreApplication.translate("DataRecorderWidget", u"Frame", None))
        self.dataRecSettingsGroupBox.setTitle(QCoreApplication.translate("DataRecorderWidget", u"Data Recorder", None))
        self.channel1Label.setText(QCoreApplication.translate("DataRecorderWidget", u"Channel 1:", None))
        self.channekl2Label.setText(QCoreApplication.translate("DataRecorderWidget", u"Channel 2:", None))
        self.recDurationLabel.setText(QCoreApplication.translate("DataRecorderWidget", u"Duration:", None))
        self.recDurationSpinBox.setSuffix(QCoreApplication.translate("DataRecorderWidget", u" ms", None))
        self.samplingPeriodLabel.setText(QCoreApplication.translate("DataRecorderWidget", u"Sampling Period", None))
        self.samplePeriodSpinBox.setSuffix(QCoreApplication.translate("DataRecorderWidget", u" ms", None))
        self.historyLabel.setText(QCoreApplication.translate("DataRecorderWidget", u"Keep History", None))
        self.historyCheckBox.setText("")
        self.clearPlotButton.setText(QCoreApplication.translate("DataRecorderWidget", u"Clear Plot", None))
    # retranslateUi

