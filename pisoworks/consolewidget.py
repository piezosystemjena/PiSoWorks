from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QKeyEvent, QTextCursor, QTextOption, QFont, QTextCharFormat, QColor


class Console(QTextEdit):
    """
    A custom console widget that emulates a command-line interface.

    Features:
    - Accepts user input and emits a signal when Enter is pressed.
    - Maintains a history of entered commands and allows navigation via arrow keys.
    - Displays output from external sources (e.g. a remote device).
    """

    command_entered: Signal = Signal(str)

    def __init__(self, parent=None) -> None:
        """
        Initializes the console widget.
        """
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setUndoRedoEnabled(False)
        self.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)

        # Set fixed-width font
        font = QFont("Consolas")  # or use "Monospace" / "Courier" depending on platform
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)  # Set to desired size
        self.setFont(font)

        self.history: list[str] = []
        self.history_index: int = -1
        self.prompt: str = ">>> "
        self.prompt_count = 0  # Count of prompts inserted
        self.insert_prompt()  # Ensure prompt is present on initialization
        self.command_help : dict[str, str] = {}


    def _ensure_prompt_present(self) -> None:
        """
        Ensures that the prompt is present at the end of the console.
        This is used after command processing, in case the handler did not insert it.
        """
        if not self.prompt_count:
            self.insert_prompt()

    def insert_prompt(self) -> None:
        """
        Inserts a new command prompt at the end of the console.
        """
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        if not self.document().isEmpty():
            cursor.insertText("\n") 
        cursor.insertText(self.prompt)
        self.move_cursor_to_end()
        self.prompt_count += 1


    def show_help(self, command: str) -> None:
        """
        Displays help information for available commands.
        If no specific command is provided, lists all commands with their help descriptions.
        If one or more commands are specified (comma-separated), displays help for each specified command.
        If a command is not recognized, notifies that no help is available for that command.
        Args:
            command (str): The input string containing 'help' and optionally a comma-separated list of commands.
        Returns:
            None
        """
        parts = command.split(',', 1)  # Split into ['help', 'cl,set'] or just ['help']
        
        output_lines = []
        if len(parts) == 1 or not parts[1].strip():
            # No parameters given, print all commands with help
            for cmd, help_text in self.command_help.items():
                output_lines.append(f"{cmd}\t{help_text}")
        else:
            # Parameters given, split by commas and print help for each
            cmds = [c.strip().lower() for c in parts[1].split(',')]
            for cmd in cmds:
                help_text = self.command_help.get(cmd)
                if help_text:
                    output_lines.append(f"{cmd}: {help_text}")
                else:
                    output_lines.append(f"No help available for '{cmd}'.")
        
        self.print_output('\n'.join(output_lines))
        return


    def execute_command(self) -> None:
        """
        Extracts and executes the current command entered in the console widget.
        Strips off the prompt (e.g. >>>) and emits `command_entered`.
        Adds the command to the history and ensures the prompt is reset.
        """
        cursor = self.textCursor()
        block = cursor.block()
        line_text = block.text()
        command = line_text[len(self.prompt.lstrip('\n\r\t')):].strip()

        self.move_cursor_to_end()

        if command:
            self.history.append(command)
            self.history_index = len(self.history)

        if command.lower() == "cls":
            self.clear_console()
            return
        
        if command.lower().startswith("help"):
            self.show_help(command)
            return

        self.prompt_count = 0  # Reset prompt count after command entry
        self.command_entered.emit(command)
        self._ensure_prompt_present()  # Ensure prompt is present after command processing



    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handles key events for Enter, Up, and Down arrows.
        Emits a signal when Enter is pressed with the input command.
        """
        cursor = self.textCursor()

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.execute_command()

        elif event.key() == Qt.Key_Up:
            if self.history and self.history_index > 0:
                self.history_index -= 1
                self.replace_current_line(self.history[self.history_index])

        elif event.key() == Qt.Key_Down:
            if self.history and self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.replace_current_line(self.history[self.history_index])
            elif self.history_index == len(self.history) - 1:
                self.history_index += 1
                self.replace_current_line("")

        elif event.key() == Qt.Key_Backspace:
            # Prevent backspace if cursor is before or within the prompt
            if cursor.positionInBlock() <= len(self.prompt):
                return  # Ignore the backspace
            else:
                super().keyPressEvent(event)

        else:
            super().keyPressEvent(event)

    def replace_current_line(self, text: str) -> None:
        """
        Replaces the current input line with the given text.
        Used for navigating through command history.

        :param text: The text to replace the current line with.
        """
        cursor = self.textCursor()
        block = cursor.block()  # Get the current text block (line)
        
        cursor.beginEditBlock()  # Begin grouped undo action

        # Select the entire block (line)
        cursor.setPosition(block.position())
        cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)

        # Replace line text
        cursor.removeSelectedText()
        cursor.insertText(self.prompt + text)
        cursor.endEditBlock()

    def move_cursor_to_end(self) -> None:
        """
        Moves the text cursor to the end of the document.
        """
        cursor: QTextCursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    def print_output(self, text: str) -> None:
        """
        Appends output to the console. If the text starts with 'error',
        it is printed in red.
        """
        # Insert formatted text
        if not text:
            self.insert_prompt()
            return
        
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.beginEditBlock()

        # Determine formatting
        fmt = QTextCharFormat()
        if text.lower().startswith("error"):
            fmt.setForeground(QColor("red"))
        else:
             fmt.setForeground(QColor("#aaaaaa"))  # Default color

        cursor.insertText("\n" + text, fmt)
        fmt.setForeground(QColor("white"))
        cursor.insertText("\n", fmt)
        cursor.endEditBlock()

        # Optionally scroll to the bottom
        self.moveCursor(QTextCursor.End)
        
        # Insert prompt if needed
        self.insert_prompt()
    
    def clear_console(self) -> None:
        """
        Clears the console output and inserts a new prompt.

        This method removes all existing text from the console widget and displays a fresh prompt for user input.
        """
        self.clear()
        self.insert_prompt()

    def register_commands(self, help_dict: dict[str, str]) -> None:
        """
        Registers a dictionary mapping command names to help messages.
        """
        self.command_help = help_dict