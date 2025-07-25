from typing import Callable, Optional
from enum import Enum, auto
from PySide6.QtWidgets import QMainWindow, QMenu
from PySide6.QtGui import QAction

class MenuID(Enum):
    """Identifiers for standard main menu categories."""
    FILE = auto()
    VIEW = auto()
    HELP = auto()
    # Add more as needed

class ActionManager:
    """
    A global action manager to decouple widgets from the main window.
    Allows widgets to register actions without directly importing or
    referencing the QMainWindow, avoiding circular imports.
    """

    def __init__(self) -> None:
        self._main_window : QMainWindow | None = None
        self._menus: dict[MenuID, QMenu] = {}


    def register_main_window(self, main_window: QMainWindow) -> None:
        """
        Registers the main application window so that actions can be inserted into its menu bar.

        Args:
            main_window (QMainWindow): The main window instance that owns the menu bar.
        """
        self._main_window = main_window

    
    def register_menu(self, menu_id: MenuID, menu: QMenu) -> None:
        """
        Registers a QMenu under a given MenuID.

        Args:
            menu_id (MenuID): Identifier for the menu.
            menu (QMenu): The menu instance created and owned by the main window.
        """
        self._menus[menu_id] = menu


    def add_action_to_menu(self, menu_id: MenuID, action: QAction) -> bool:
        """
        Adds a ready-made QAction to the specified menu.

        Args:
            menu_id (MenuID): Target menu identifier.
            action (QAction): The action to insert.

        Returns:
            bool: True if added successfully, False otherwise.
        """
        menu = self._menus.get(menu_id)
        if not menu:
            print(f"ActionManager: Menu '{menu_id.name}' not registered.")
            return False

        menu.addAction(action)
        return True

# Singleton instance
action_manager = ActionManager()