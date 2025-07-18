from PySide6.QtWidgets import QFrame, QComboBox

from nv200.data_recorder import DataRecorder, DataRecorderSource

from pysoworks.ui_data_recorder_widget import Ui_DataRecorderWidget
from pysoworks.mplcanvas import MplCanvas
from pysoworks.mplcanvas import NavigationToolbar2QT
from pysoworks.mplcanvas import MplWidget
from pysoworks.ui_helpers import get_icon


class DataRecorderWidget(QFrame):

    DEFAULT_RECORDING_DURATION_MS : int = 120  # Default recording duration in milliseconds
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DataRecorderWidget()
        ui = self.ui
        ui.setupUi(self)
        ui.mplWidget.setStyleSheet("") # clear designer stylesheet
        self.canvas = ui.mplWidget.canvas # forward the canvas object

        ui.recDurationSpinBox.valueChanged.connect(self.update_sampling_period)
        ui.recDurationSpinBox.setValue(self.DEFAULT_RECORDING_DURATION_MS)
        ui.clearPlotButton.setIcon(get_icon("delete", size=24, fill=True))
        ui.historyCheckBox.setChecked(True)
        self.init_recording_source_combobox(ui.channel1ComboBox)
        self.init_recording_source_combobox(ui.channel2ComboBox)
        self.update_sampling_period()

    
    def init_recording_source_combobox(self, cb : QComboBox):
        """
        Initializes the recording source combobox with available data sources.
        
        Args:
            combobox (QComboBox): The combobox to populate with data sources.
        """
        cb.clear()
        for source in DataRecorderSource:
            cb.addItem(str(source), source.value)

        
    def update_sampling_period(self):
        """
        Updates the sampling period in the waveform generator based on the given value.

        Args:
            value (int): The new sampling period in milliseconds.
        """
        ui = self.ui
        sample_period = DataRecorder.get_sample_period_ms_for_duration(ui.recDurationSpinBox.value())
        ui.samplePeriodSpinBox.setValue(sample_period)


    def set_recording_duration_ms(self, duration_ms: float):
        """
        Sets the recording duration in the data recorder.

        Args:
            duration_ms (int): The recording duration in milliseconds.
        """
        ui = self.ui
        ui.recDurationSpinBox.setValue(duration_ms)
