import pandas as pd

from PySide6.QtWidgets import QWidget, QComboBox, QCheckBox, QDoubleSpinBox, QFileDialog, QMessageBox
from PySide6.QtGui import QAction, QPalette
from PySide6.QtCore import Signal, QStandardPaths

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
        self.ui.importButton.clicked.connect(self._on_import_button_clicked)

        self._custom_waveform = None  # Placeholder for custom waveform data


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
        tracker.add_widget(ui.waveSamplingPeriodSpinBox)

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
        ui.levelSpacer.changeSize(0, 0 if is_custom else 10)

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


    def _on_import_button_clicked(self):
        """
        Handles the event when the import button is clicked to import custom waveform data.
        """
        self._custom_waveform = self._import_custom_waveform()
        self.waveform_widget_change_tracker.set_all_widgets_dirty(True)
        self._on_value_changed()  # Notify that options have changed

    
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

        repolish(ui.waveSamplingPeriodSpinBox)
        

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


    def _import_custom_waveform(self):
        """
        Opens a file dialog to import custom waveform data and stores it.
        """
        home_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)
        file_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Import Waveform File",
            home_dir,
            "CSV and Excel Files (*.csv *.xlsx);;CSV Files (*.csv);;Excel Files (*.xlsx)",
            "CSV and Excel Files (*.csv *.xlsx)"  # default filter
        )
        
        if file_path is None or file_path == "":
            return  # User cancelled the dialog
        
        try:
            values = self._parse_custom_waveform(file_path)
            return values
        except ValueError as e:
            QMessageBox.critical(self, "Import Error", str(e))
            return None


    def _parse_custom_waveform(self, file_path: str, max_values: int = 1024) -> list[float]:
        """
        Reads a single-column CSV or Excel file containing percentage values (0-100).

        If the number of values exceeds max_values, asks the user whether to truncate
        or resample the data to fit the max_values limit.

        Args:
            parent (QWidget): Parent widget for dialogs.
            file_path (str): Path to CSV or Excel file.
            max_values (int): Maximum allowed number of values (default 1024).

        Returns:
            List[float]: List of percentage values as floats.

        Raises:
            ValueError: For invalid data or unsupported file types.
        """
        # Load data
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type. Provide a .csv or Excel (.xls/.xlsx) file.")

        if df.shape[1] != 1:
            raise ValueError(f"Expected exactly one column, found {df.shape[1]} columns.")

        # Validate and extract values
        col = df.iloc[:, 0]
        col_numeric = pd.to_numeric(col, errors='coerce')

        if col_numeric.isnull().any():
            raise ValueError("Column contains non-numeric or invalid values.")

        if not ((col_numeric >= 0) & (col_numeric <= 100)).all():
            raise ValueError("Waveform values are given in percent and must be in the range 0 to 100 inclusive.")

        values = col_numeric.tolist()

        # Check length limit
        if len(values) > max_values:
            # Ask user what to do
            msg = QMessageBox(self)
            msg.setWindowTitle("Too many values")
            msg.setText(f"The data has {len(values)} values, which exceeds the limit of {max_values}.")
            msg.setInformativeText("Do you want to truncate the data or resample it?")
            truncate_button = msg.addButton("Truncate", QMessageBox.ButtonRole.AcceptRole)
            resample_button = msg.addButton("Resample", QMessageBox.ButtonRole.AcceptRole)
            cancel_button = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
            msg.setDefaultButton(truncate_button)
            msg.exec()

            clicked = msg.clickedButton()

            if clicked == cancel_button:
                raise ValueError("User cancelled operation due to too many values.")

            elif clicked == truncate_button:
                # Truncate list
                values = values[:max_values]

            elif clicked == resample_button:
                # Resample by skipping values to reduce to max_values
                factor = (len(values) + max_values - 1) // max_values  # ceiling division
                values = values[::factor]

                # Ensure result not longer than max_values (edge case)
                values = values[:max_values]

        return values

    
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


    def set_sampling_period_step(self, value):
        """
        Sets the sampling period step value.
        """
        self.ui.waveSamplingPeriodSpinBox.setSingleStep(value)
        self.ui.waveSamplingPeriodSpinBox.setMinimum(value)

    
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
    

    def set_dirty(self):
        """
        Sets all tracked widgets to dirty state.
        """
        return self.waveform_widget_change_tracker.set_all_widgets_dirty(True)

    
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
        self._set_sampling_period_readonly(self.sampling_period_readonly)

    
    def set_show_dirty_indicators(self, show: bool):
        """
        Enables or disables the display of dirty indicators for all tracked widgets.
        """
        self.waveform_widget_change_tracker.set_show_dirty_indicators(show)


    def set_dirty_tracking(self, enabled: bool):
        """
        Enables or disables dirty tracking for all tracked widgets.
        """
        self.waveform_widget_change_tracker.set_enable_dirty_tracking(enabled)


    def get_custom_waveform_data(self):
        """
        Returns the custom waveform data if applicable.
        """
        return self._custom_waveform