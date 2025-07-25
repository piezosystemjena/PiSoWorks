from xml.sax import handler
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
from PySide6.QtCore import QObject, Signal



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

    dirtyStateChanged: Signal = Signal(bool)
    """Signal emitted when the dirty state changes."""

    widget_handlers: Dict[
        Type[QWidget],
        Tuple[str, Callable[[QWidget], Any], Callable[[QWidget, Any], None]],
    ] = {
        QDoubleSpinBox: (
            "valueChanged",
            lambda w: w.value(),
            lambda w, v: w.setValue(float(v)),
        ),
        QSpinBox: (
            "valueChanged",
            lambda w: w.value(),
            lambda w, v: w.setValue(int(v)),
        ),
        QCheckBox: (
            "stateChanged",
            lambda w: w.isChecked(),
            lambda w, v: w.setChecked(bool(v)),
        ),
        QComboBox: (
            "currentIndexChanged",
            lambda w: w.currentIndex(),
            lambda w, v: w.setCurrentIndex(int(v)),
        ),
    }

    @classmethod
    def register_widget_handler(cls,
        widget_type: Type[QWidget],
        signal_name: str,
        value_getter: Callable[[QWidget], Any],
        value_setter: Callable[[QWidget, Any], None]
    ) -> None:
        """
        Register a custom widget type with its signal and value getter.

        Args:
            widget_type: The QWidget subclass to track.
            signal_name: Name of the signal to connect (e.g. 'valueChanged').
            value_getter: Function that returns the widget's current value.
        """
        cls.widget_handlers[widget_type] = (signal_name, value_getter, value_setter)


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
        self.backups: Dict[str, Dict[QWidget, Any]] = {} # a dictionary of named backups
        self.widgets: List[QWidget] = []
        self.dirty_widgets: set[QWidget] = set()


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
        for widget_type, (signal_name, _, _) in self.widget_handlers.items():
            if isinstance(widget, widget_type):
                signal = getattr(widget, signal_name)
                signal.connect(lambda _, w=widget: self._check_dirty(w))
                return
        raise TypeError(f"Unsupported widget type: {type(widget)}")


    def _get_value(self, widget: QWidget) -> Any:
        """
        Get the current value of the widget.
        """
        widget_type = type(widget)

        # Try exact type match first (fast path)
        handler = self.widget_handlers.get(widget_type)
        if handler is not None:
            _, getter, _ = handler
            return getter(widget)

        # Fallback: check if widget is instance of any registered base type (slower)
        for registered_type, (_, getter, _) in self.widget_handlers.items():
            if isinstance(widget, registered_type):
                return getter(widget) 
        raise TypeError(f"No value accessor registered for: {widget_type}")
            

    def _set_value(self, widget: QWidget, value: Any) -> None:
        """
        Set the value of the widget if supported.
        
        Args:
            widget: The widget to set the value for.
            value: The value to set.
        
        Raises:
            TypeError: If the widget type is not supported.
        """
        widget_type = type(widget)
        handler = self.widget_handlers.get(widget_type)
        if handler is not None:
            _, _, setter = handler
            setter(widget, value)

        for registered_type, (_, _, setter) in self.widget_handlers.items():
            if isinstance(widget, registered_type):
                setter(widget, value)
                return
        raise TypeError(f"No value accessor registered for: {widget_type}")
    

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
    

    def set_value_of_widget(self, widget: QWidget, value: Any) -> None:
        """
        Set the value of the given widget if supported.

        Args:
            widget: The widget to update.
            value: The value to set.

        Raises:
            TypeError: If the widget type is not supported.
        """
        self._set_value(widget, value)
    

    def get_initial_value_of_widget(self, widget: QWidget) -> Any:
        """
        Get the initial value of a widget when it was first registered.

        Args:
            widget: The widget to query.

        Returns:
            The initial value of the widget.
        
        Raises:
            ValueError: If the widget is not being tracked.
        """
        if widget not in self.initial_values:
            raise ValueError(f"Widget {widget} is not being tracked.")
        return self.initial_values[widget]
    

    def _set_dirty(self, widget: QWidget, dirty: bool) -> None:
        """
        Set the 'dirty' property of the widget and refresh its style.
        
        Args:
            widget: The widget to update.
            dirty: True to mark as dirty, False to clear.
        """
        widget.setProperty("dirty", dirty)
        self._refresh_style(widget)
        if dirty:
            self.dirty_widgets.add(widget)
        else:
            self.dirty_widgets.discard(widget)


    def _check_dirty(self, widget: QWidget) -> None:
        """
        Check if the widget is dirty and set the 'dirty' property accordingly.
        """
        old_dirty = self.has_dirty_widgets()
        current = self._get_value(widget)
        initial = self.initial_values.get(widget)
        is_dirty = current != initial
        self._set_dirty(widget, is_dirty)
        self._emit_dirty_state_changed(old_dirty)


    def _refresh_style(self, widget: QWidget) -> None:
        """
        Re-apply the widget's style to reflect dynamic property changes.
        """
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()


    def _emit_dirty_state_changed(self, old_dirty: bool) -> None:
        """
        Emit the dirtyStateChanged signal if the dirty state has changed.
        
        Args:
            old_dirty: Previous dirty state.
        """
        new_dirty = self.has_dirty_widgets()
        if new_dirty != old_dirty:
            self.dirtyStateChanged.emit(new_dirty)


    def capture_initial_values(self) -> None:
        """
        Set current widget values as the new initial values and clear dirty flags.
        """
        for widget in self.widgets:
            self.initial_values[widget] = self._get_value(widget)
            self._set_dirty(widget, False)
        self._emit_dirty_state_changed(False)


    def backup_current_values(self, backup_name : str) -> None:
        """
        Store the current values of all tracked widgets in a backup dictionary.

        Args:
            backup_name: Name of the backup to store values under.
        """
        self.backups[backup_name] = {widget: self._get_value(widget) for widget in self.widgets}


    def backup_initial_values(self, backup_name: str) -> None:
        """
        Store the initial values of all tracked widgets in a backup dictionary.

        Args:
            backup_name: Name of the backup to store initial values under.
        """
        self.backups[backup_name] = self.initial_values.copy()    


    def restore_backup(self, backup_name: str) -> None:
        """
        Restore the values of all tracked widgets from a named backup.

        Args:
            backup_name: Name of the backup to restore.
        
        Raises:
            KeyError: If the backup does not exist.
        """
        if backup_name not in self.backups:
            raise KeyError(f"No backup found with name '{backup_name}'.")

        backup = self.backups[backup_name]
        for widget, value in backup.items():
            self._set_value(widget, value)
                

    def reset(self) -> None:
        """
        Clear the dirty state of all tracked widgets.
        """
        old_dirty = self.has_dirty_widgets()
        for widget in self.widgets:
            self.initial_values[widget] = self._get_value(widget)
            self._set_dirty(widget, False)
        self._emit_dirty_state_changed(old_dirty)


    def set_all_widgets_dirty(self, dirty: bool = True) -> None:
        """
        Set the 'dirty' property for all tracked widgets.
        """
        old_dirty = self.has_dirty_widgets()
        for widget in self.widgets:
            self._set_dirty(widget, dirty)
            self.initial_values[widget] = "__dirty__"
        self.dirtyStateChanged.emit(dirty)
        self._emit_dirty_state_changed(old_dirty)


    def undo_changes(self) -> None:
        """
        Revert all tracked widgets to their initial values.
        """
        for widget in self.widgets:
            initial_value = self.initial_values.get(widget)
            if initial_value is not None:
                self._set_value(widget, initial_value)
                self._set_dirty(widget, False)
        self._emit_dirty_state_changed(True)


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
    

    def has_dirty_widgets(self) -> bool:
        """
        Check if there are any widgets currently marked as dirty.

        Returns:
            True if at least one widget is dirty, False otherwise.
        """
        return bool(self.dirty_widgets)
