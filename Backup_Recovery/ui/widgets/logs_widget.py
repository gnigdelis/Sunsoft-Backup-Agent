from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
)

from PySide6.QtCore import (
    QCoreApplication,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)

from ui.styles.theme import (
    LOGS_BACKGROUND,
    WHITE_COLOR,
    LOG_FONT_SIZE,
)


class LogsWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout()

        panel = PanelWidget(
            "Ζωντανές Καταγραφές Backup"
        )

        self.logs_textbox = QTextEdit()

        self.logs_textbox.setMinimumHeight(
            250
        )

        self.logs_textbox.setMaximumHeight(
            250
        )

        self.logs_textbox.setReadOnly(
            True
        )

        self.logs_textbox.setPlaceholderText(
            "Το Backup δεν έχει ξεκινήσει ακόμη..."
        )

        self.logs_textbox.setStyleSheet(

            f"""

            QTextEdit {{

                background-color: {LOGS_BACKGROUND};

                color: {WHITE_COLOR};

                border: none;

                padding: 10px;

                font-size: {LOG_FONT_SIZE}pt;

            }}

            """

        )

        self.logs_textbox.append(
            "INFO | Το Sunsoft Backup είναι έτοιμο."
        )

        panel.add_widget(
            self.logs_textbox
        )

        main_layout.addWidget(
            panel
        )

        self.setLayout(
            main_layout
        )

    def add_log(
        self,
        message,
    ):

        with open(
            "logs_widget_debug.log",
            "a",
            encoding="utf-8",
        ) as file:

            file.write(message + "\n")

        self.logs_textbox.append(
            message
        )

        scrollbar = (
            self.logs_textbox.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )

        QCoreApplication.processEvents()

    def add_info_log(
        self,
        message,
    ):

        self.add_log(
            f"INFO | {message}"
        )

    def add_success_log(
        self,
        message,
    ):

        self.add_log(
            f"SUCCESS | {message}"
        )

    def add_warning_log(
        self,
        message,
    ):

        self.add_log(
            f"WARNING | {message}"
        )

    def add_error_log(
        self,
        message,
    ):

        self.add_log(
            f"ERROR | {message}"
        )

    def clear_logs(self):

        self.logs_textbox.clear()
