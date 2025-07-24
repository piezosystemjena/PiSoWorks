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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QLabel,
    QLayout, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

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

        self.samplePeriodSpinBox = QDoubleSpinBox(self.dataRecSettingsGroupBox)
        self.samplePeriodSpinBox.setObjectName(u"samplePeriodSpinBox")
        sizePolicy.setHeightForWidth(self.samplePeriodSpinBox.sizePolicy().hasHeightForWidth())
        self.samplePeriodSpinBox.setSizePolicy(sizePolicy)
        self.samplePeriodSpinBox.setReadOnly(True)
        self.samplePeriodSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.samplePeriodSpinBox.setMaximum(16777215.000000000000000)

        self.gridLayout.addWidget(self.samplePeriodSpinBox, 1, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.recDurationSpinBox = QSpinBox(self.dataRecSettingsGroupBox)
        self.recDurationSpinBox.setObjectName(u"recDurationSpinBox")
        sizePolicy.setHeightForWidth(self.recDurationSpinBox.sizePolicy().hasHeightForWidth())
        self.recDurationSpinBox.setSizePolicy(sizePolicy)
        self.recDurationSpinBox.setMinimum(1)
        self.recDurationSpinBox.setMaximum(16777215)

        self.gridLayout.addWidget(self.recDurationSpinBox, 0, 3, 1, 1)

        self.recDurationLabel = QLabel(self.dataRecSettingsGroupBox)
        self.recDurationLabel.setObjectName(u"recDurationLabel")
        self.recDurationLabel.setStyleSheet(u"margin-left: 6px")

        self.gridLayout.addWidget(self.recDurationLabel, 0, 2, 1, 1)

        self.channel1Label = QLabel(self.dataRecSettingsGroupBox)
        self.channel1Label.setObjectName(u"channel1Label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.channel1Label.sizePolicy().hasHeightForWidth())
        self.channel1Label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.channel1Label, 0, 0, 1, 1)

        self.channekl2Label = QLabel(self.dataRecSettingsGroupBox)
        self.channekl2Label.setObjectName(u"channekl2Label")
        sizePolicy1.setHeightForWidth(self.channekl2Label.sizePolicy().hasHeightForWidth())
        self.channekl2Label.setSizePolicy(sizePolicy1)
        self.channekl2Label.setStyleSheet(u"")

        self.gridLayout.addWidget(self.channekl2Label, 1, 0, 1, 1)

        self.recsrc2ComboBox = QComboBox(self.dataRecSettingsGroupBox)
        self.recsrc2ComboBox.setObjectName(u"recsrc2ComboBox")

        self.gridLayout.addWidget(self.recsrc2ComboBox, 1, 1, 1, 1)

        self.samplingPeriodLabel = QLabel(self.dataRecSettingsGroupBox)
        self.samplingPeriodLabel.setObjectName(u"samplingPeriodLabel")
        self.samplingPeriodLabel.setStyleSheet(u"margin-left: 6px")

        self.gridLayout.addWidget(self.samplingPeriodLabel, 1, 2, 1, 1)


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
#if QT_CONFIG(tooltip)
        self.recsrc1ComboBox.setToolTip(QCoreApplication.translate("DataRecorderWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">Recorder Channel 1</span></p><p>Choose the source for high-frequency data (up to 20 kHz) recorded by device channel 1.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.samplePeriodSpinBox.setToolTip(QCoreApplication.translate("DataRecorderWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">Sampling Period</span></p><p>Calculated based on the total recording duration and available memory.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.samplePeriodSpinBox.setSuffix(QCoreApplication.translate("DataRecorderWidget", u" ms", None))
#if QT_CONFIG(tooltip)
        self.recDurationSpinBox.setToolTip(QCoreApplication.translate("DataRecorderWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">Recording Duration</span></p><p>Set the total duration for the internal data recorder. Longer durations result in lower sampling frequencies due to memory limits.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.recDurationSpinBox.setSuffix(QCoreApplication.translate("DataRecorderWidget", u" ms", None))
        self.recDurationLabel.setText(QCoreApplication.translate("DataRecorderWidget", u"Duration:", None))
        self.channel1Label.setText(QCoreApplication.translate("DataRecorderWidget", u"Channel 1:", None))
        self.channekl2Label.setText(QCoreApplication.translate("DataRecorderWidget", u"Channel 2:", None))
#if QT_CONFIG(tooltip)
        self.recsrc2ComboBox.setToolTip(QCoreApplication.translate("DataRecorderWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">Recorder Channel 2</span></p><p>Choose the source for high-frequency data (up to 20 kHz) recorded by device channel 2.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.samplingPeriodLabel.setText(QCoreApplication.translate("DataRecorderWidget", u"Sampling Period", None))
    # retranslateUi

