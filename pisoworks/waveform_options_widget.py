from PySide6.QtWidgets import QWidget, QComboBox, QCheckBox, QDoubleSpinBox
from PySide6.QtGui import QAction, QPalette
from PySide6.QtCore import Signal

from nv200.data_recorder import DataRecorder, DataRecorderSource
from nv200.waveform_generator import WaveformType

from pisoworks.ui_waveform_options_widget import Ui_WaveformOptionsWidget
from pisoworks.ui_helpers import get_icon, set_combobox_index_by_value, repolish
from pisoworks.style_manager import style_manager
from pisoworks.input_widget_change_tracker import InputWidgetChangeTracker

class WaveformOptionsWidget(QWidget):

    dirtyStateChanged: Signal = Signal(bool, object)
    optionChanged: Signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_WaveformOptionsWidget()
        self.ui.setupUi(self)

        self.sampling_period_readonly = False

        self._init_waveform_combobox()
        self._init_tracker()

        self.ui.waveFormComboBox.currentIndexChanged.connect(self._on_value_changed)
        self.ui.freqSpinBox.valueChanged.connect(self._on_value_changed)
        self.ui.waveSamplingPeriodSpinBox.valueChanged.connect(self._on_value_changed)
        self.ui.phaseShiftSpinBox.valueChanged.connect(self._on_value_changed)
        self.ui.dutyCycleSpinBox.valueChanged.connect(self._on_value_changed)
        self.ui.lowLevelSpinBox.valueChanged.connect(self._on_value_changed)
        self.ui.highLevelSpinBox.valueChanged.connect(self._on_value_changed)


    def _init_tracker(self):
        """
        Initializes the input widget change tracker for monitoring widget state changes.
        """
        self.waveform_widget_change_tracker: InputWidgetChangeTracker = InputWidgetChangeTracker(self)
        tracker = self.waveform_widget_change_tracker
        ui = self.ui

        tracker.add_widget(ui.waveFormComboBox)
        tracker.add_widget(ui.freqSpinBox)
        tracker.add_widget(ui.phaseShiftSpinBox)
        tracker.add_widget(ui.dutyCycleSpinBox)
        tracker.add_widget(ui.lowLevelSpinBox)
        tracker.add_widget(ui.highLevelSpinBox)

        tracker.set_all_widgets_dirty()  # set all widgets to dirty initially
        tracker.dirtyStateChanged.connect(self._on_dirty_state_changed)

    
    def _init_waveform_combobox(self):
        """
        Initializes the waveform type combo box with available waveform options.
        """
        cb = self.ui.waveFormComboBox
        cb.clear()
        cb.addItem("Sine", WaveformType.SINE)
        cb.addItem("Triangle", WaveformType.TRIANGLE)
        cb.addItem("Square", WaveformType.SQUARE)
        cb.addItem("Custom", -1)
        cb.currentIndexChanged.connect(self._on_waveform_type_changed)  # Show duty cycle only for square wave
        self._on_waveform_type_changed(cb.currentIndex())  # Initialize visibility based on the current selection

    
    def _on_waveform_type_changed(self, index: int):
        """
        Handles the event when the waveform type combo box is changed.
        """
        ui = self.ui
        duty_visible = (index == WaveformType.SQUARE.value)
        ui.dutyCycleLabel.setVisible(duty_visible)
        ui.dutyCycleSpinBox.setVisible(duty_visible)

        is_custom = (index == (WaveformType.SQUARE.value + 1))
        ui.customLabel.setVisible(is_custom)
        ui.importButton.setVisible(is_custom)

        ui.freqLabel.setVisible(not is_custom)
        ui.freqSpinBox.setVisible(not is_custom)

        self._set_sampling_period_readonly(not is_custom)

        repolish(ui.waveSamplingPeriodSpinBox)

        ui.phaseLabel.setVisible(not is_custom)
        ui.phaseShiftSpinBox.setVisible(not is_custom)
        ui.highLabel.setVisible(not is_custom)
        ui.highLevelSpinBox.setVisible(not is_custom)
        ui.lowLabel.setVisible(not is_custom)
        ui.lowLevelSpinBox.setVisible(not is_custom)

    
    def _set_sampling_period_readonly(self, readonly: bool):
        """
        Sets the readonly state of the sampling period spin box.
        """
        ui = self.ui
        value = readonly or self.sampling_period_readonly

        ui.waveSamplingPeriodSpinBox.setReadOnly(value)

        if ui.waveSamplingPeriodSpinBox.isReadOnly():
            ui.waveSamplingPeriodSpinBox.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        else:
            ui.waveSamplingPeriodSpinBox.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.UpDownArrows)


    def _on_value_changed(self):
        """
        Handles the event when any widget value is changed and emits the optionChanged signal.
        """
        self.optionChanged.emit()

    
    def _on_dirty_state_changed(self, value):
        """
        Handles the event when the dirty state of tracked widgets changes.
        """
        self.dirtyStateChanged.emit(value, self)

    
    def get_waveform_type(self):
        """
        Returns the currently selected waveform type.
        """
        return self.ui.waveFormComboBox.currentData()


    def get_frequency(self):
        """
        Returns the current frequency value.
        """
        return self.ui.freqSpinBox.value()
    

    def get_sampling_period(self):
        """
        Returns the current sampling period value.
        """
        return self.ui.waveSamplingPeriodSpinBox.value()
    

    def get_phase_shift(self):
        """
        Returns the current phase shift value.
        """
        return self.ui.phaseShiftSpinBox.value()

    
    def get_duty_cycle(self):
        """
        Returns the current duty cycle value.
        """
        return self.ui.dutyCycleSpinBox.value()
    

    def get_low_level(self):
        """
        Returns the current low level value.
        """
        return self.ui.lowLevelSpinBox.value()    
    

    def get_high_level(self):
        """
        Returns the current high level value.
        """
        return self.ui.highLevelSpinBox.value()
    

    def set_waveform_type(self, waveform_type):
        """
        Sets the waveform type in the combo box.
        """
        set_combobox_index_by_value(self.ui.waveFormComboBox, waveform_type)

    
    def set_frequency(self, value):
        """
        Sets the frequency value.
        """
        self.ui.freqSpinBox.setValue(value)


    def set_sampling_period(self, value):
        """
        Sets the sampling period value.
        """
        self.ui.waveSamplingPeriodSpinBox.setValue(value)

    
    def set_phase_shift(self, value):
        """
        Sets the phase shift value.
        """
        self.ui.phaseShiftSpinBox.setValue(value)


    def set_duty_cycle(self, value):
        """
        Sets the duty cycle value.
        """
        self.ui.dutyCycleSpinBox.setValue(value)

    
    def set_high_level(self, value):
        """
        Sets the high level value.
        """
        self.ui.highLevelSpinBox.setValue(value)


    def set_low_level(self, value):
        """
        Sets the low level value.
        """
        self.ui.lowLevelSpinBox.setValue(value)


    def set_setpoint_options(self, unit, setpoint_range):
        """
        Sets the unit and range options for the low and high level setpoint spin boxes.
        """
        ui = self.ui

        ui.lowLevelSpinBox.setRange(setpoint_range[0], setpoint_range[1])
        ui.lowLevelSpinBox.setValue(setpoint_range[0])
        ui.lowLevelSpinBox.setSuffix(f" {unit}")
        ui.highLevelSpinBox.setRange(setpoint_range[0], setpoint_range[1])
        ui.highLevelSpinBox.setValue(setpoint_range[1])
        ui.highLevelSpinBox.setSuffix(f" {unit}")


    def is_dirty(self):
        """
        Returns whether any tracked widgets have been modified.
        """
        return self.waveform_widget_change_tracker.has_dirty_widgets()

    
    def clear_dirty(self):
        """
        Clears the dirty state of all tracked widgets.
        """
        return self.waveform_widget_change_tracker.set_all_widgets_dirty(False)
    

    def set_sampling_period_readonly(self, readonly: bool):
        """
        Sets the external readonly flag for the sampling period spin box.
        """
        self.sampling_period_readonly = readonly
        self._set_sampling_period_readonly(not self.sampling_period_readonly)


    def set_dirty_tracking(self, enabled: bool):
        """
        Enables or disables dirty tracking for all tracked widgets.
        """
        self.waveform_widget_change_tracker.set_enable_dirty_tracking(enabled)
