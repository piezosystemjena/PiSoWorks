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
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QLabel, QLayout, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from pysoworks.mplcanvas import MplWidget

class Ui_DataRecorderWidget(object):
    def setupUi(self, DataRecorderWidget):
        if not DataRecorderWidget.objectName():
            DataRecorderWidget.setObjectName(u"DataRecorderWidget")
        DataRecorderWidget.resize(1071, 774)
        self.verticalLayout = QVBoxLayout(DataRecorderWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.dataRecSettingsGroupBox = QGroupBox(DataRecorderWidget)
        self.dataRecSettingsGroupBox.setObjectName(u"dataRecSettingsGroupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataRecSettingsGroupBox.sizePolicy().hasHeightForWidth())
        self.dataRecSettingsGroupBox.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.dataRecSettingsGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(-1, -1, -1, 9)
        self.recsrc1ComboBox = QComboBox(self.dataRecSettingsGroupBox)
        self.recsrc1ComboBox.setObjectName(u"recsrc1ComboBox")

        self.gridLayout.addWidget(self.recsrc1ComboBox, 0, 1, 1, 1)

        self.channel1Label = QLabel(self.dataRecSettingsGroupBox)
        self.channel1Label.setObjectName(u"channel1Label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.channel1Label.sizePolicy().hasHeightForWidth())
        self.channel1Label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.channel1Label, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.samplePeriodSpinBox = QDoubleSpinBox(self.dataRecSettingsGroupBox)
        self.samplePeriodSpinBox.setObjectName(u"samplePeriodSpinBox")
        sizePolicy.setHeightForWidth(self.samplePeriodSpinBox.sizePolicy().hasHeightForWidth())
        self.samplePeriodSpinBox.setSizePolicy(sizePolicy)
        self.samplePeriodSpinBox.setReadOnly(True)
        self.samplePeriodSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.samplePeriodSpinBox.setMaximum(16777215.000000000000000)

        self.gridLayout.addWidget(self.samplePeriodSpinBox, 1, 3, 1, 1)

        self.historyCheckBox = QCheckBox(self.dataRecSettingsGroupBox)
        self.historyCheckBox.setObjectName(u"historyCheckBox")
        self.historyCheckBox.setChecked(False)
        self.historyCheckBox.setProperty(u"toggleSwitch", True)

        self.gridLayout.addWidget(self.historyCheckBox, 0, 6, 1, 1)

        self.samplingPeriodLabel = QLabel(self.dataRecSettingsGroupBox)
        self.samplingPeriodLabel.setObjectName(u"samplingPeriodLabel")
        self.samplingPeriodLabel.setStyleSheet(u"margin-left: 6px")

        self.gridLayout.addWidget(self.samplingPeriodLabel, 1, 2, 1, 1)

        self.channekl2Label = QLabel(self.dataRecSettingsGroupBox)
        self.channekl2Label.setObjectName(u"channekl2Label")
        sizePolicy1.setHeightForWidth(self.channekl2Label.sizePolicy().hasHeightForWidth())
        self.channekl2Label.setSizePolicy(sizePolicy1)
        self.channekl2Label.setStyleSheet(u"")

        self.gridLayout.addWidget(self.channekl2Label, 1, 0, 1, 1)

        self.clearPlotButton = QPushButton(self.dataRecSettingsGroupBox)
        self.clearPlotButton.setObjectName(u"clearPlotButton")
        sizePolicy.setHeightForWidth(self.clearPlotButton.sizePolicy().hasHeightForWidth())
        self.clearPlotButton.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.clearPlotButton, 1, 5, 1, 3)

        self.recDurationLabel = QLabel(self.dataRecSettingsGroupBox)
        self.recDurationLabel.setObjectName(u"recDurationLabel")
        self.recDurationLabel.setStyleSheet(u"margin-left: 6px")

        self.gridLayout.addWidget(self.recDurationLabel, 0, 2, 1, 1)

        self.historyLabel = QLabel(self.dataRecSettingsGroupBox)
        self.historyLabel.setObjectName(u"historyLabel")

        self.gridLayout.addWidget(self.historyLabel, 0, 5, 1, 1)

        self.recDurationSpinBox = QSpinBox(self.dataRecSettingsGroupBox)
        self.recDurationSpinBox.setObjectName(u"recDurationSpinBox")
        sizePolicy.setHeightForWidth(self.recDurationSpinBox.sizePolicy().hasHeightForWidth())
        self.recDurationSpinBox.setSizePolicy(sizePolicy)
        self.recDurationSpinBox.setMinimum(1)
        self.recDurationSpinBox.setMaximum(5000)

        self.gridLayout.addWidget(self.recDurationSpinBox, 0, 3, 1, 1)

        self.recsrc2ComboBox = QComboBox(self.dataRecSettingsGroupBox)
        self.recsrc2ComboBox.setObjectName(u"recsrc2ComboBox")

        self.gridLayout.addWidget(self.recsrc2ComboBox, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.dataRecSettingsGroupBox)

        self.mplWidget = MplWidget(DataRecorderWidget)
        self.mplWidget.setObjectName(u"mplWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.mplWidget.sizePolicy().hasHeightForWidth())
        self.mplWidget.setSizePolicy(sizePolicy2)
        self.mplWidget.setStyleSheet(u"background: lightgrey")

        self.verticalLayout.addWidget(self.mplWidget)


        self.retranslateUi(DataRecorderWidget)

        QMetaObject.connectSlotsByName(DataRecorderWidget)
    # setupUi

    def retranslateUi(self, DataRecorderWidget):
        DataRecorderWidget.setWindowTitle(QCoreApplication.translate("DataRecorderWidget", u"Frame", None))
        self.dataRecSettingsGroupBox.setTitle(QCoreApplication.translate("DataRecorderWidget", u"Data Recorder", None))
        self.channel1Label.setText(QCoreApplication.translate("DataRecorderWidget", u"Channel 1:", None))
        self.samplePeriodSpinBox.setSuffix(QCoreApplication.translate("DataRecorderWidget", u" ms", None))
        self.historyCheckBox.setText("")
        self.samplingPeriodLabel.setText(QCoreApplication.translate("DataRecorderWidget", u"Sampling Period", None))
        self.channekl2Label.setText(QCoreApplication.translate("DataRecorderWidget", u"Channel 2:", None))
        self.clearPlotButton.setText(QCoreApplication.translate("DataRecorderWidget", u"Clear Plot", None))
        self.recDurationLabel.setText(QCoreApplication.translate("DataRecorderWidget", u"Duration:", None))
        self.historyLabel.setText(QCoreApplication.translate("DataRecorderWidget", u"Keep History", None))
        self.recDurationSpinBox.setSuffix(QCoreApplication.translate("DataRecorderWidget", u" ms", None))
    # retranslateUi

