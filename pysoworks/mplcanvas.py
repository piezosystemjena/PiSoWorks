from typing import Sequence, Union
from matplotlib import lines
import numpy as np
import csv
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.colors import to_rgba
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PySide6.QtCore import QStandardPaths, QTimer
from PySide6.QtGui import QPalette, QColor, QAction
from PySide6.QtWidgets import QVBoxLayout, QWidget, QFileDialog
from nv200.data_recorder import DataRecorder
from pysoworks.ui_helpers import get_icon


def mpl_color(color: QColor) -> tuple[float, float, float, float]:
    """
    Converts a QColor to a tuple of floats in the range 0.0–1.0.
    """
    return (
        color.redF(),   # R in 0.0–1.0
        color.greenF(),
        color.blueF(),
        color.alphaF()
    )


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

        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self.update_layout)


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
        self._resize_timer.start(100)  # 250 ms after last resize event


    def update_layout(self):
        """
        Updates the layout of the figure to ensure proper spacing and alignment.
        This method is useful after adding or modifying elements in the figure.
        """
        new_size = self.size()
        if new_size.width() > 0 and new_size.height() > 0:  # avoid singular matrix
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


    def autoscale(self, axis: int = 0):
        """
        Automatically adjusts the axis limits to fit the plotted data.
        Parameters:
            axis (int, optional): The index of the axis to autoscale. Defaults to 0.
        This method enables autoscaling for the specified axis, resets the x and y axis limits,
        recalculates the data limits, updates the view, and redraws the canvas to reflect the changes.
        """
        ax = self.get_axes(axis)
        ax.set_autoscale_on(True)       # Turns autoscale mode back on
        ax.set_xlim(auto=True)          # Reset x-axis limits
        ax.set_ylim(auto=True)          # Reset y-axis limits

        # Autoscale the axes after plotting the data
        ax.relim()
        ax.autoscale_view()

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


    def set_dark_mode(self, dark_mode: bool):
        """
        Sets the dark mode for the canvas.
        
        Args:
            dark_mode (bool): If True, sets the canvas to dark mode; otherwise, sets it to light mode.
        """
        # Define colors
        bg_color = 'black' if dark_mode else 'white'
        fg_color = 'darkgray'  # Used for ticks, labels, spines, and grid
        text_color = mpl_color(QPalette().color(QPalette.ColorRole.WindowText))
  
        # Update figure background
        self._fig.patch.set_facecolor(bg_color)

        # Update all axes in axes_list
        for ax in self.axes_list:
            ax.set_facecolor(bg_color)
            ax.tick_params(colors=fg_color)
            ax.xaxis.label.set_color(text_color)
            ax.yaxis.label.set_color(text_color)
            ax.title.set_color(text_color)

            # Update axes spines
            for spine in ax.spines.values():
                spine.set_color(fg_color)

            # Update tick label colors
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_color(text_color)

        self._fig.canvas.draw_idle()  # Redraw the canvas

    
    def create_export_data(self) -> pd.DataFrame | None:
        """
        Exports the data from all lines in the first axes as a pandas DataFrame.
        The method handles two cases:
        1. If all lines have identical X data arrays and lengths, the DataFrame will have one X column and one column per line's Y data.
        2. If lines have different X data arrays or lengths, the DataFrame will use the union of all X values, aligning Y data accordingly and filling missing values with NaN (then forward-filling).
        Returns:
            pd.DataFrame | None: The exported data as a DataFrame, or None if there are no lines to export.
        """
        ax = self.axes_list[0]
        lines = ax.get_lines()

        if not lines:
            print("No data to export.")
            return

        # Gather all lines' lengths and X data
        lengths = [len(line.get_xdata()) for line in lines]
        all_lengths_equal = all(length == lengths[0] for length in lengths)

        # Check if all lines have identical X data arrays (if lengths equal)
        if all_lengths_equal:
            base_x = lines[0].get_xdata()
            all_x_same = all(np.array_equal(line.get_xdata(), base_x) for line in lines)
        else:
            all_x_same = False

        if all_lengths_equal and all_x_same:
            # Simple export: all share same x and same length
            x_data = lines[0].get_xdata()
            data = {ax.get_xlabel(): x_data}
            for i, line in enumerate(lines, start=1):
                label = line.get_label()
                if not label or label.startswith("_"):
                    label = f"y{i}"
                data[label] = line.get_ydata()

            df = pd.DataFrame(data)
        else:
            # More complicated: shared full X from first line, partial Y data per line
            
            # Create union of all X data points from all lines
            all_x_values = set()
            for line in lines:
                all_x_values.update(line.get_xdata())
            full_x = np.array(sorted(all_x_values))

            x_to_index = {x_val: idx for idx, x_val in enumerate(full_x)}
            data = {ax.get_xlabel(): full_x}

            for i, line in enumerate(lines, start=1):
                line_x = line.get_xdata()
                line_y = line.get_ydata()
                label = line.get_label()
                if not label or label.startswith("_"):
                    label = f"y{i}"

                y_full = np.full_like(full_x, fill_value=np.nan, dtype=float)

                for lx, ly in zip(line_x, line_y):
                    idx = x_to_index.get(lx)
                    if idx is not None:
                        y_full[idx] = ly
                    else:
                        print(f"Warning: x value {lx} in line '{label}' not found in full X data")

                data[label] = y_full

            df = pd.DataFrame(data)
            # Forward-fill missing Y values down each column except 'x'
            df.loc[:, df.columns != "x"] = df.loc[:, df.columns != "x"].ffill()
        
        return df
    
   
    def export_plot_data(self) -> None:
        """
        Export the data from the first Matplotlib Axes in the widget's canvas to CSV or Excel.

        This function:
        - Assumes the widget has an attribute `canvas` (a Matplotlib FigureCanvas).
        - Retrieves all Line2D objects from the first axes in the figure.
        - Exports the X values and each line's Y values into a DataFrame.
        - Prompts the user to select a save location and format (*.csv or *.xlsx).
        - Automatically saves in the chosen format, defaulting to CSV if no extension is given.

        File format behavior:
        - *.csv   → saved with `DataFrame.to_csv(index=False)`
        - *.xlsx  → saved with `DataFrame.to_excel(index=False)` (requires openpyxl)

        Dependencies:
        pip install pandas openpyxl

        Raises:
        AttributeError: If `self.canvas` is missing or is not a Matplotlib FigureCanvas.
        """
        df = self.create_export_data()
        if df is None:
            return

        home_dir = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save Data",
            home_dir,
            "CSV Files (*.csv);;Excel Files (*.xlsx)",
            "Excel Files (*.xlsx)"
        )

        if not file_path:
            return

        if "csv" in selected_filter.lower():
            if not file_path.lower().endswith(".csv"):
                file_path += ".csv"
            df.to_csv(file_path, index=False)
            print(f"Data exported to CSV: {file_path}")

        elif "xlsx" in selected_filter.lower():
            if not file_path.lower().endswith(".xlsx"):
                file_path += ".xlsx"
            df.to_excel(file_path, index=False)
            print(f"Data exported to Excel: {file_path}")


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
            #'configure_subplots': 'line_axis',
            'configure_subplots': '-',
            'edit_parameters': 'tune',
        }

        for action_name, icon_path in icon_paths.items():
            action = self._actions.get(action_name)
            if action:
                if icon_path == "-":
                    # Remove action if icon path is "-"
                    self.removeAction(action)
                else:
                    icon = get_icon(
                        icon_path,
                        size=24,
                        fill=False,
                        color=QPalette.ColorRole.WindowText
                    )
                    action.setIcon(icon)

    def set_dark_mode(self, dark_mode: bool):
        """
        Sets the dark mode for the toolbar.
        
        Args:
            dark_mode (bool): If True, sets the toolbar to dark mode; otherwise, sets it to light mode.
        """
        self._initialize_icons() 


class MplWidget(QWidget):
    '''
    Widget promoted and defined in Qt Designer
    '''
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas(self)
        # Create the navigation toolbar linked to the canvas
        self.toolbar = LightIconToolbar(self.canvas, self)
        self.export_action : QAction | None = None
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

    def show_export_action(self):
        """
        Shows the export to CSV action.
        """
        if self.export_action:
            return
        self.export_action = a = QAction(get_icon('export_notes', size=24, fill=False, color=QPalette.ColorRole.WindowText), "Export to Excel / CSV", self)
        self.add_toolbar_action(a)
        a.triggered.connect(self.canvas.export_plot_data)

    def add_toolbar_separator(self):
        """
        Adds a separator to the toolbar.
        """
        action = QAction(self)
        action.setSeparator(True)
        self.toolbar.add_custom_action(action)


    def set_dark_mode(self, dark_mode: bool):
        """
        Sets the dark mode for the canvas and toolbar.
        
        Args:
            dark_mode (bool): If True, sets the canvas and toolbar to dark mode; otherwise, sets them to light mode.
        """
        self.canvas.set_dark_mode(dark_mode)
        self.toolbar.set_dark_mode(dark_mode)


    
