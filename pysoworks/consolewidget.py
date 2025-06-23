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
        self.setWordWrapMode(QTextOption.WrapAnywhere)

        # Set fixed-width font
        font = QFont("Consolas")  # or use "Monospace" / "Courier" depending on platform
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)  # Set to desired size
        self.setFont(font)

        self.history: list[str] = []
        self.history_index: int = -1
        self.prompt: str = ">>> "
        self.prompt_count = 0  # Count of prompts inserted
        self.insert_prompt()  # Ensure prompt is present on initialization


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
        cursor.movePosition(QTextCursor.End)
        if not self.document().isEmpty():
            cursor.insertText("\n") 
        cursor.insertText(self.prompt)
        self.move_cursor_to_end()
        self.prompt_count += 1



    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handles key events for Enter, Up, and Down arrows.
        Emits a signal when Enter is pressed with the input command.
        """
        cursor = self.textCursor()

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            cursor = self.textCursor()
            #cursor.movePosition(QTextCursor.End)
            block = cursor.block()
            line_text = block.text()
            command = line_text[len(self.prompt.lstrip('\n\r\t')):].strip()

            self.move_cursor_to_end()

            if command:
                self.history.append(command)
                self.history_index = len(self.history)

            self.prompt_count = 0  # Reset prompt count after command entry
            self.command_entered.emit(command)
            self._ensure_prompt_present()  # Ensure prompt is present after command processing

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
    