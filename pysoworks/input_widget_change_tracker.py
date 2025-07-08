from PySide6.QtWidgets import (
    QWidget,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QComboBox,
)
from PySide6.QtCore import QObject


from typing import Callable, Any, Dict, List, Type, Tuple
from PySide6.QtWidgets import QWidget, QDoubleSpinBox, QCheckBox, QComboBox
from PySide6.QtCore import QObject



class InputWidgetChangeTracker(QObject):
    """
    Tracks changes in input widgets by setting a dynamic 'dirty' property
    when their value differs from the stored initial value.

    Widgets must be styled externally using:
        QWidget[dirty="true"] { background-color: lightyellow; }

    Supported widgets:
    - QDoubleSpinBox
    - QCheckBox
    - QComboBox
    """

    widget_handlers: Dict[Type[QWidget], Tuple[str, Callable[[QWidget], Any]]] = {
        QDoubleSpinBox: ("valueChanged", lambda w: w.value()),
        QSpinBox: ("valueChanged", lambda w: w.value()),
        QCheckBox: ("stateChanged", lambda w: w.isChecked()),
        QComboBox: ("currentIndexChanged", lambda w: w.currentIndex()),
    }

    @classmethod
    def register_widget_handler(cls,
        widget_type: Type[QWidget],
        signal_name: str,
        value_getter: Callable[[QWidget], Any]
    ) -> None:
        """
        Register a custom widget type with its signal and value getter.

        Args:
            widget_type: The QWidget subclass to track.
            signal_name: Name of the signal to connect (e.g. 'valueChanged').
            value_getter: Function that returns the widget's current value.
        """
        cls.widget_handlers[widget_type] = (signal_name, value_getter)


    @classmethod
    def supported_widget_types(cls) -> list[Type[QWidget]]:
        """
        Returns a list of all currently supported QWidget types.

        These are the widget classes that can be tracked by the tracker.
        """
        return list(cls.widget_handlers.keys())


    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.initial_values: Dict[QWidget, Any] = {}
        self.widgets: List[QWidget] = []


    def add_widget(
        self, widget: QWidget) -> None:
        """
        Register a widget to track, with optional apply function.

        Args:
            widget: Widget to track.
            apply_func: Optional callable to apply widget value.
        """
        if widget in self.widgets:
            return
        
        self.widgets.append(widget)
        self.initial_values[widget] = self._get_value(widget)
        self._connect_signal(widget)

    def _connect_signal(self, widget: QWidget) -> None:
        """
        Connect the widget's change signal to dirty-check logic.
        """
        for widget_type, (signal_name, _) in self.widget_handlers.items():
            if isinstance(widget, widget_type):
                signal = getattr(widget, signal_name)
                signal.connect(lambda _, w=widget: self._check_dirty(w))
                return
        raise TypeError(f"Unsupported widget type: {type(widget)}")

    def _get_value(self, widget: QWidget) -> Any:
        """
        Get the current value of the widget.
        """
        for widget_type, (_, value_func) in self.widget_handlers.items():
            if isinstance(widget, widget_type):
                return value_func(widget)
        raise TypeError(f"No value accessor registered for: {type(widget)}")
    
    def get_value_of_widget(self, widget: QWidget) -> Any:
        """
        Return the current value of the given widget if supported.

        Args:
            widget: The widget to query.

        Returns:
            The current value of the widget.

        Raises:
            TypeError: If the widget type is not supported.
        """
        return self._get_value(widget)
    
    def _set_dirty(self, widget: QWidget, dirty: bool) -> None:
        """
        Set the 'dirty' property of the widget and refresh its style.
        
        Args:
            widget: The widget to update.
            dirty: True to mark as dirty, False to clear.
        """
        widget.setProperty("dirty", dirty)
        self._refresh_style(widget)

    def _check_dirty(self, widget: QWidget) -> None:
        """
        Check if the widget is dirty and set the 'dirty' property accordingly.
        """
        current = self._get_value(widget)
        initial = self.initial_values.get(widget)
        is_dirty = current != initial
        self._set_dirty(widget, is_dirty)

    def _refresh_style(self, widget: QWidget) -> None:
        """
        Re-apply the widget's style to reflect dynamic property changes.
        """
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()


    def capture_initial_values(self) -> None:
        """
        Set current widget values as the new initial values and clear dirty flags.
        """
        for widget in self.widgets:
            self.initial_values[widget] = self._get_value(widget)
            self._set_dirty(widget, False)


    def reset(self) -> None:
        """
        Clear the dirty state of all tracked widgets.
        """
        for widget in self.widgets:
            self.initial_values[widget] = self._get_value(widget)
            self._set_dirty(widget, False)


    def reset_widget(self, widget: QWidget) -> None:
        """
        Reset a specific widget's dirty state and initial value.

        Args:
            widget: The widget to reset.
        """
        if widget in self.widgets:
            self.initial_values[widget] = self._get_value(widget)
            self._set_dirty(widget, False)
        else:
            raise ValueError(f"Widget {widget} is not being tracked.")


    def get_dirty_widgets(self) -> List[QWidget]:
        """
        Returns a list of all widgets currently marked as dirty.

        Returns:
            List of widgets with property 'dirty' == True.
        """
        return [w for w in self.widgets if w.property("dirty") is True]
