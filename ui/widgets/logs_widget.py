from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
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

        #
        # MAIN LAYOUT
        #

        main_layout = QVBoxLayout()

        #
        # PANEL
        #

        panel = PanelWidget(
            "Ζωντανές Καταγραφές Backup"
        )

        #
        # LOGS TEXTBOX
        #

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

        #
        # LOGS STYLE
        #

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

        #
        # DEFAULT MESSAGE
        #

        self.logs_textbox.append(
            "INFO | Το Sunsoft Backup είναι έτοιμο."
        )

        #
        # ADD WIDGET
        #

        panel.add_widget(
            self.logs_textbox
        )

        #
        # ADD PANEL
        #

        main_layout.addWidget(
            panel
        )

        #
        # SET LAYOUT
        #

        self.setLayout(
            main_layout
        )

    #
    # GENERIC LOG
    #

    def add_log(
        self,
        message,
    ):

        self.logs_textbox.append(
            message
        )

        scrollbar = (
            self.logs_textbox.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )

    #
    # INFO LOG
    #

    def add_info_log(
        self,
        message,
    ):

        self.add_log(
            f"INFO | {message}"
        )

    #
    # SUCCESS LOG
    #

    def add_success_log(
        self,
        message,
    ):

        self.add_log(
            f"SUCCESS | {message}"
        )

    #
    # WARNING LOG
    #

    def add_warning_log(
        self,
        message,
    ):

        self.add_log(
            f"WARNING | {message}"
        )

    #
    # ERROR LOG
    #

    def add_error_log(
        self,
        message,
    ):

        self.add_log(
            f"ERROR | {message}"
        )

    #
    # CLEAR LOGS
    #

    def clear_logs(self):

        self.logs_textbox.clear()