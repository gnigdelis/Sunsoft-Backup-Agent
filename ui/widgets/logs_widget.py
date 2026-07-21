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
            "INFO | Ο Sunsoft Backup Agent είναι έτοιμος."
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

    def add_log(
        self,
        message: str,
    ):

        self.logs_textbox.append(
            message
        )

        #
        # AUTO SCROLL
        #

        scrollbar = self.logs_textbox.verticalScrollBar()

        scrollbar.setValue(
            scrollbar.maximum()
        )

    def clear_logs(self):

        self.logs_textbox.clear()