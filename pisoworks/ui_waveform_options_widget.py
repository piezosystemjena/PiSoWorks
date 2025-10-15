# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'waveform_options_widget.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDoubleSpinBox,
    QFormLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_WaveformOptionsWidget(object):
    def setupUi(self, WaveformOptionsWidget):
        if not WaveformOptionsWidget.objectName():
            WaveformOptionsWidget.setObjectName(u"WaveformOptionsWidget")
        WaveformOptionsWidget.resize(238, 287)
        self.formLayout = QFormLayout(WaveformOptionsWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.wavefomLabel = QLabel(WaveformOptionsWidget)
        self.wavefomLabel.setObjectName(u"wavefomLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.wavefomLabel)

        self.waveFormComboBox = QComboBox(WaveformOptionsWidget)
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.addItem("")
        self.waveFormComboBox.setObjectName(u"waveFormComboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.waveFormComboBox)

        self.verticalSpacer_6 = QSpacerItem(167, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout.setItem(1, QFormLayout.ItemRole.SpanningRole, self.verticalSpacer_6)

        self.freqLabel = QLabel(WaveformOptionsWidget)
        self.freqLabel.setObjectName(u"freqLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.freqLabel)

        self.freqSpinBox = QDoubleSpinBox(WaveformOptionsWidget)
        self.freqSpinBox.setObjectName(u"freqSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freqSpinBox.sizePolicy().hasHeightForWidth())
        self.freqSpinBox.setSizePolicy(sizePolicy)
        self.freqSpinBox.setMinimum(0.010000000000000)
        self.freqSpinBox.setMaximum(100000.000000000000000)
        self.freqSpinBox.setValue(20.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.freqSpinBox)

        self.waveSamplingPeriodLabel = QLabel(WaveformOptionsWidget)
        self.waveSamplingPeriodLabel.setObjectName(u"waveSamplingPeriodLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.waveSamplingPeriodLabel)

        self.waveSamplingPeriodSpinBox = QDoubleSpinBox(WaveformOptionsWidget)
        self.waveSamplingPeriodSpinBox.setObjectName(u"waveSamplingPeriodSpinBox")
        self.waveSamplingPeriodSpinBox.setReadOnly(False)
        self.waveSamplingPeriodSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.waveSamplingPeriodSpinBox.setMaximum(3276.800000000000182)
        self.waveSamplingPeriodSpinBox.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.waveSamplingPeriodSpinBox)

        self.customLabel = QLabel(WaveformOptionsWidget)
        self.customLabel.setObjectName(u"customLabel")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.customLabel)

        self.importButton = QPushButton(WaveformOptionsWidget)
        self.importButton.setObjectName(u"importButton")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.importButton)

        self.phaseLabel = QLabel(WaveformOptionsWidget)
        self.phaseLabel.setObjectName(u"phaseLabel")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.phaseLabel)

        self.phaseShiftSpinBox = QDoubleSpinBox(WaveformOptionsWidget)
        self.phaseShiftSpinBox.setObjectName(u"phaseShiftSpinBox")
        sizePolicy.setHeightForWidth(self.phaseShiftSpinBox.sizePolicy().hasHeightForWidth())
        self.phaseShiftSpinBox.setSizePolicy(sizePolicy)
        self.phaseShiftSpinBox.setDecimals(3)
        self.phaseShiftSpinBox.setMinimum(0.000000000000000)
        self.phaseShiftSpinBox.setMaximum(360.000000000000000)
        self.phaseShiftSpinBox.setValue(0.000000000000000)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.phaseShiftSpinBox)

        self.dutyCycleLabel = QLabel(WaveformOptionsWidget)
        self.dutyCycleLabel.setObjectName(u"dutyCycleLabel")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.dutyCycleLabel)

        self.dutyCycleSpinBox = QDoubleSpinBox(WaveformOptionsWidget)
        self.dutyCycleSpinBox.setObjectName(u"dutyCycleSpinBox")
        self.dutyCycleSpinBox.setDecimals(1)
        self.dutyCycleSpinBox.setMinimum(0.100000000000000)
        self.dutyCycleSpinBox.setValue(50.000000000000000)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.dutyCycleSpinBox)

        self.verticalSpacer_5 = QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.formLayout.setItem(7, QFormLayout.ItemRole.FieldRole, self.verticalSpacer_5)

        self.highLabel = QLabel(WaveformOptionsWidget)
        self.highLabel.setObjectName(u"highLabel")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.highLabel)

        self.highLevelSpinBox = QDoubleSpinBox(WaveformOptionsWidget)
        self.highLevelSpinBox.setObjectName(u"highLevelSpinBox")
        sizePolicy.setHeightForWidth(self.highLevelSpinBox.sizePolicy().hasHeightForWidth())
        self.highLevelSpinBox.setSizePolicy(sizePolicy)
        self.highLevelSpinBox.setDecimals(3)
        self.highLevelSpinBox.setMaximum(1000.000000000000000)

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.highLevelSpinBox)

        self.lowLabel = QLabel(WaveformOptionsWidget)
        self.lowLabel.setObjectName(u"lowLabel")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.lowLabel)

        self.lowLevelSpinBox = QDoubleSpinBox(WaveformOptionsWidget)
        self.lowLevelSpinBox.setObjectName(u"lowLevelSpinBox")
        sizePolicy.setHeightForWidth(self.lowLevelSpinBox.sizePolicy().hasHeightForWidth())
        self.lowLevelSpinBox.setSizePolicy(sizePolicy)
        self.lowLevelSpinBox.setDecimals(3)
        self.lowLevelSpinBox.setMaximum(1000.000000000000000)

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.lowLevelSpinBox)


        self.retranslateUi(WaveformOptionsWidget)

        QMetaObject.connectSlotsByName(WaveformOptionsWidget)
    # setupUi

    def retranslateUi(self, WaveformOptionsWidget):
        self.wavefomLabel.setText(QCoreApplication.translate("WaveformOptionsWidget", u"Waveform", None))
        self.waveFormComboBox.setItemText(0, QCoreApplication.translate("WaveformOptionsWidget", u"Sine", None))
        self.waveFormComboBox.setItemText(1, QCoreApplication.translate("WaveformOptionsWidget", u"Triangle", None))
        self.waveFormComboBox.setItemText(2, QCoreApplication.translate("WaveformOptionsWidget", u"Square", None))
        self.waveFormComboBox.setItemText(3, QCoreApplication.translate("WaveformOptionsWidget", u"Custom", None))

        self.freqLabel.setText(QCoreApplication.translate("WaveformOptionsWidget", u"Freq.", None))
        self.freqSpinBox.setSuffix(QCoreApplication.translate("WaveformOptionsWidget", u" Hz", None))
        self.waveSamplingPeriodLabel.setText(QCoreApplication.translate("WaveformOptionsWidget", u"Sampling Period", None))
        self.waveSamplingPeriodSpinBox.setSuffix(QCoreApplication.translate("WaveformOptionsWidget", u" ms", None))
        self.customLabel.setText(QCoreApplication.translate("WaveformOptionsWidget", u"Cust. Waveform", None))
        self.importButton.setText(QCoreApplication.translate("WaveformOptionsWidget", u"Load CSV / Excel", None))
        self.phaseLabel.setText(QCoreApplication.translate("WaveformOptionsWidget", u"Phase Shift", None))
        self.phaseShiftSpinBox.setSuffix(QCoreApplication.translate("WaveformOptionsWidget", u" \u00b0", None))
        self.dutyCycleLabel.setText(QCoreApplication.translate("WaveformOptionsWidget", u"Duty Cycle", None))
        self.dutyCycleSpinBox.setSuffix(QCoreApplication.translate("WaveformOptionsWidget", u" %", None))
        self.highLabel.setText(QCoreApplication.translate("WaveformOptionsWidget", u"High Level", None))
        self.lowLabel.setText(QCoreApplication.translate("WaveformOptionsWidget", u"Low Level", None))
        pass
    # retranslateUi

