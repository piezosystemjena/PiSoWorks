from typing import Sequence, Union
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.colors import to_rgba
from matplotlib.axes import Axes
from matplotlib.backend_tools import ToolBase, ToolToggleBase
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PySide6.QtGui import QPalette, QColor, QAction
from PySide6.QtWidgets import QVBoxLayout, QWidget, QApplication
from nv200.data_recorder import DataRecorder
from qt_material_icons import MaterialIcon
from pysoworks.ui_helpers import get_icon


class MplCanvas(FigureCanvas):
    '''
    Class to represent the FigureCanvas widget for integration of Matplotlib with Qt.
    '''
    _fig: Figure = None

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.style.use('dark_background')
        self._fig = Figure(figsize=(width, height), dpi=dpi)
        self._fig.tight_layout()
        self.ax1 = self._fig.add_subplot(111)
        self.axes_list : list[Axes] = [self.ax1]
        self._fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        ax = self.ax1
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Value')
        self.init_axes_object(ax)

        self.ax2 : Axes | None = None  # Secondary axis for two-line plots
        super().__init__(self._fig)


    def init_axes_object(self, ax : Axes):
        """
        Initializes the appearance of the given Matplotlib Axes object.
        This method configures the grid, spine colors, and tick parameters
        to use a dark gray color scheme for improved visual consistency.
        Args:
            ax (Axes): The Matplotlib Axes object to be styled.
        """
        ax.grid(True, color='darkgray', linestyle='--', linewidth=0.5)
        ax.spines['top'].set_color('darkgray')
        ax.spines['right'].set_color('darkgray')
        ax.spines['bottom'].set_color('darkgray')
        ax.spines['left'].set_color('darkgray')

        # Set tick parameters for dark grey color
        ax.tick_params(axis='x', colors='darkgray')
        ax.tick_params(axis='y', colors='darkgray')


    def get_axes(self, index : int) -> Axes:
        """
        Retrieve the matplotlib Axes object at the specified index.

        Args:
            index (int): The index of the axes to retrieve. 
                - 0: Returns the primary axes.
                - 1: Returns the secondary axes if it exists, or creates it if it does not.

        Returns:
            Axes: The requested matplotlib Axes object.

        Raises:
            IndexError: If the index is not 0 or 1.
        """
        if index < len(self.axes_list):
            return self.axes_list[index]
        
        if index == 1:
            self.ax2 = self.ax1.twinx()
            self.init_axes_object(self.ax2)
            self.axes_list.append(self.ax2)
            return self.ax2

        raise IndexError(f"Index {index} out of range for axes list.")


    def resizeEvent(self, event):
        """
        Handles the widget's resize event.

        Calls the parent class's resizeEvent to ensure default behavior,
        then updates the layout to maintain proper spacing and appearance
        after the widget has been resized.

        Args:
            event (QResizeEvent): The resize event containing the new size information.
        """
        super().resizeEvent(event)
        self.update_layout()  # Update layout on resize to ensure proper spacing


    def update_layout(self):
        """
        Updates the layout of the figure to ensure proper spacing and alignment.
        This method is useful after adding or modifying elements in the figure.
        """
        self._fig.tight_layout()
        self.draw()


    def set_plot_title(self, title: str):
        """
        Sets the title of the plot.

        Args:
            title (str): The title to set for the plot.
        """
        self.ax1.set_title(title)  # Set title with dark gray color
        self.update_layout


    def plot_recorder_data(self, rec_data : DataRecorder.ChannelRecordingData, color : QColor = QColor('orange'), axis : int = 0):
        """
        Plots the data and stores the line object for later removal.
        """
        self.remove_all_axes_lines(axis)  # Remove all previous lines before plotting new data
        self.add_recorder_data_line(rec_data, color, axis)  # Add the new line to the plot


    def add_recorder_data_line(self, rec_data : DataRecorder.ChannelRecordingData, color : QColor = QColor('orange'), axis : int = 0):
        """
        Adds a new line plot to the canvas using the provided channel recording data.
        """
        self.add_line(rec_data.sample_times_ms, rec_data.values, str(rec_data.source), color, axis)  # Add the new line to the plot


    def plot_data(self, x_data: Union[Sequence[float], np.ndarray], y_data: Union[Sequence[float], np.ndarray], label: str, color : QColor = QColor('orange'), axis : int = 0):
        """
        Plots the data and stores the line object for later removal.
        """
        self.remove_all_axes_lines(axis)  # Remove all previous lines before plotting new data
        self.add_line(x_data, y_data, label, color, axis)  # Add the new line to the plot


    def add_line(self, x_data: Sequence[float], y_data: Sequence[float], label: str, color : QColor = QColor('orange'), axis : int = 0):
        """
        Adds a new line plot to the canvas 
        """
        # Plot the data and add a label for the legend
        ax = self.get_axes(axis)

        rgba = (
            color.redF(),   # R in 0.0–1.0
            color.greenF(),
            color.blueF(),
            color.alphaF()
        )
        
        print(f"Adding line with color: {rgba} and label: {label}")
        line, = ax.plot(
            x_data, y_data, 
            linestyle='-', color=rgba, label=label
        )

        ax.set_autoscale_on(True)       # Turns autoscale mode back on
        ax.set_xlim(auto=True)          # Reset x-axis limits
        ax.set_ylim(auto=True)          # Reset y-axis limits

        # Autoscale the axes after plotting the data
        ax.relim()
        ax.autoscale_view()
        
        #Show the legend with custom styling
        ax.legend(
            facecolor='darkgray', 
            edgecolor='darkgray', 
            frameon=True, 
            loc='best', 
            fontsize=10
        )

        # Redraw the canvas
        self.update_layout()
   
    def update_line(self, line_index: int, x_data: Sequence[float], y_data: Sequence[float], axis : int = 0):
        """
        Updates the data of a specific line in the plot.
        """
        ax = self.get_axes(axis)
        lines = ax.get_lines()
        
        if 0 <= line_index < len(lines):
            line = lines[line_index]
            line.set_xdata(x_data)
            line.set_ydata(y_data)

            # Rescale the axes to fit the new data
            ax.relim()
            ax.autoscale_view()

            # Redraw the canvas to reflect the changes
            self.draw()
        else:
            raise IndexError("Line index out of range.")


    def get_line_color(self, line_index: int, axis : int = 0) -> QColor:
        """
        Returns the color of a specific line in the plot.
        """
        ax = self.get_axes(axis)
        lines = ax.get_lines()
        
        if 0 <= line_index < len(lines):
            line = lines[line_index]
            mpl_color = line.get_color()
            r, g, b, a = to_rgba(mpl_color)
            qcolor = QColor.fromRgbF(r, g, b, a)
            return qcolor
        else:
            raise IndexError("Line index out of range.")


    def set_line_color(self, line_index: int, color: QColor, axis : int = 0):
        """
        Sets the color of a specific line in the plot.
        """
        ax = self.get_axes(axis)
        lines = ax.get_lines()
        
        if 0 <= line_index < len(lines):
            line = lines[line_index]
            rgba = (
                color.redF(),   # R in 0.0–1.0
                color.greenF(),
                color.blueF(),
                color.alphaF()
            )
            print(f"Setting line color: {rgba}")
            line.set_color(rgba)
            self.draw()


    def get_lines(self, axis: int = 0) -> Sequence:
        """
        Returns a sequence of all lines in the plot.
        """
        ax = self.get_axes(axis)
        return ax.get_lines()
    

    def get_line_count(self, axis: int = 0) -> int:
        """
        Returns the number of lines in the plot.
        """
        ax = self.get_axes(axis)
        return len(ax.get_lines())


    def scale_axes(self, x_min: float, x_max: float, y_min: float, y_max: float, axis: int = 0):
        """
        Scales the axes to the specified limits.
        """
        ax = self.get_axes(axis)
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        # Redraw the canvas to reflect the changes
        self.draw()    

    def remove_all_axes_lines(self, axis: int = 0):
        """Removes all lines from the axes."""
        if axis >= len(self.axes_list):
            return

        ax = self.axes_list[axis]
        # Iterate over all lines in the axes and remove them
        for line in ax.get_lines():
            line.remove()

        # Redraw the canvas to reflect the change
        self.draw()


    def clear_plot(self):
        """
        Clears the plot by removing all lines and resetting the axes.
        """
        self.remove_all_axes_lines(0)
        self.remove_all_axes_lines(1)





class LightIconToolbar(NavigationToolbar2QT):
    """
    A customized Matplotlib navigation toolbar for Qt applications with light-themed icons.
    This toolbar extends the default NavigationToolbar2QT to provide:
    - Custom icons for standard navigation actions (home, back, forward, pan, zoom, save, etc.)
    - A custom "Clear Plot" action with its own icon.
    - Icon initialization on first show event to ensure proper styling.
    """
    _icons_initialized : bool = False

    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)


    def add_custom_action(self, action: QAction, index : int = -1):
        """
        Adds a custom action to the toolbar at the specified index.
        
        Args:
            index (int): The position to insert the action. Defaults to -1 (end of the toolbar).
            action (QAction): The action to add. If None, a default action is created.
        """
        self.insertAction(self.actions()[index], action)
            

    def showEvent(self, event):
        super().showEvent(event)
        if not self._icons_initialized:
            self._initialize_icons()
            self._icons_initialized = True

    def _initialize_icons(self):
        icon_paths = {
            'home': 'home',
            'back': 'arrow_back',
            'forward': 'arrow_forward',
            'pan': 'pan_tool',
            'zoom': 'zoom_in',
            'save_figure': 'file_save',
            'configure_subplots': 'line_axis',
            'edit_parameters': 'tune',
        }

        for action_name, icon_path in icon_paths.items():
            action = self._actions.get(action_name)
            if action:
                icon = get_icon(icon_path, size=24, fill=False, color=QPalette.ColorRole.WindowText)
                action.setIcon(icon)


class MplWidget(QWidget):
    '''
    Widget promoted and defined in Qt Designer
    '''
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        # Create the navigation toolbar linked to the canvas
        self.toolbar = LightIconToolbar(self.canvas, self)
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.vbl.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbl)
        self.setContentsMargins(0, 0, 0, 0)


    def add_toolbar_action(self, action: QAction):
        """
        Adds a custom action to the toolbar.
        
        Args:
            action (QAction): The action to add to the toolbar.
        """
        self.toolbar.add_custom_action(action)

    def add_toolbar_separator(self):
        """
        Adds a separator to the toolbar.
        """
        action = QAction(self)
        action.setSeparator(True)
        self.toolbar.add_custom_action(action)


    
