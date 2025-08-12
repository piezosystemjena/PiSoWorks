from PySide6.QtWidgets import QFrame, QComboBox, QCheckBox
from PySide6.QtGui import QAction, QPalette

from nv200.data_recorder import DataRecorder, DataRecorderSource

from pysoworks.ui_data_recorder_widget import Ui_DataRecorderWidget
from pysoworks.ui_helpers import get_icon, set_combobox_index_by_value
from pysoworks.style_manager import style_manager


class DataRecorderWidget(QFrame):

    DEFAULT_RECORDING_DURATION_MS : int = 120  # Default recording duration in milliseconds
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DataRecorderWidget()
        ui = self.ui
        ui.setupUi(self)
        self.recsrc_combo_boxes = [self.ui.recsrc1ComboBox, self.ui.recsrc2ComboBox]
        ui.mplWidget.setStyleSheet("") # clear designer stylesheet
        self.canvas = ui.mplWidget.canvas # forward the canvas object
        self.mpl_widget = ui.mplWidget

        ui.mplWidget.show_export_action()
        ui.mplWidget.add_toolbar_separator()
        self.clear_plot_action = a = QAction("Clear Plot", parent=self, icon=get_icon("delete", size=24, fill=False, color=QPalette.ColorRole.WindowText))
        ui.mplWidget.add_toolbar_action(a)

        cb = self.history_checkbox = QCheckBox("Keep History", self)
        cb.setObjectName("historyCheckBox")
        cb.setProperty("toggleSwitch", True)
        cb.setStyleSheet("QCheckBox#historyCheckBox { margin-left: 10px; }")
        ui.mplWidget.toolbar.addWidget(cb)
        cb.setChecked(False)

        ui.recDurationSpinBox.valueChanged.connect(self.update_sampling_period)
        ui.recDurationSpinBox.setValue(self.DEFAULT_RECORDING_DURATION_MS)
        self.init_recording_source_combobox(ui.recsrc1ComboBox, DataRecorderSource.PIEZO_VOLTAGE)
        self.init_recording_source_combobox(ui.recsrc2ComboBox, DataRecorderSource.PIEZO_POSITION)
        self.update_sampling_period()

        style_manager.style.dark_mode_changed.connect(self.set_dark_mode)

    
    def init_recording_source_combobox(self, cb : QComboBox, default_value : DataRecorderSource):
        """
        Initializes the recording source combobox with available data sources.
        
        Args:
            combobox (QComboBox): The combobox to populate with data sources.
        """
        cb.clear()
        for source in DataRecorderSource:
            cb.addItem(str(source), source)
        set_combobox_index_by_value(cb, default_value)

        
    def update_sampling_period(self):
        """
        Updates the sampling period in the waveform generator based on the given value.

        Args:
            value (int): The new sampling period in milliseconds.
        """
        ui = self.ui
        sample_period = DataRecorder.get_sample_period_ms_for_duration(ui.recDurationSpinBox.value())
        ui.samplePeriodSpinBox.setValue(sample_period)


    def set_recording_duration_ms(self, duration_ms: int):
        """
        Sets the recording duration in the data recorder.

        Args:
            duration_ms (int): The recording duration in milliseconds.
        """
        ui = self.ui
        ui.recDurationSpinBox.setValue(duration_ms)


    def get_recording_source(self, channel : int) -> DataRecorderSource:
        """
        Returns the currently selected recording source from the combobox.

        Returns:
            DataRecorderSource: The selected recording source.
        """
        return self.recsrc_combo_boxes[channel].currentData()
        

    def set_recording_source(self, channel: int, source: DataRecorderSource):
        """
        Sets the recording source in the combobox for the specified channel.

        Args:
            channel (int): The channel number (1 or 2).
            source (DataRecorderSource): The recording source to set.
        """
        set_combobox_index_by_value(self.recsrc_combo_boxes[channel], source)


    def set_dark_mode(self, dark_mode: bool):
        """
        Updates the UI if dark mode is enabled or disabled.
        """
        self.clear_plot_action.setIcon(get_icon("delete", size=24, fill=False, color=QPalette.ColorRole.WindowText))

