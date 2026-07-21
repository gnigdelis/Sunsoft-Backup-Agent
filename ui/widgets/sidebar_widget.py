from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
)

from PySide6.QtCore import Qt

from ui.styles.config import (
    APPLICATION_VERSION,
)

from ui.styles.theme import (
    SIDEBAR_BACKGROUND,
    BUTTON_BACKGROUND,
    BUTTON_HOVER_BACKGROUND,
    BUTTON_BORDER_COLOR,
    BUTTON_BORDER_RADIUS,
    BUTTON_HEIGHT,
    TEXT_FONT_SIZE,
    GOLD_COLOR,
    WHITE_COLOR,
    SECONDARY_TEXT_COLOR,
    SUCCESS_COLOR,
    STATUS_READY,
)


class SidebarWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        layout.setSpacing(
            10
        )

        #
        # APPLICATION TITLE
        #

        self.title_label = QLabel(
            "SUNSOFT"
        )

        self.subtitle_label = QLabel(
            "Backup Agent"
        )

        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.subtitle_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.subtitle_label
        )

        layout.addSpacing(
            10
        )

        #
        # SIDEBAR BUTTONS
        #

        self.dashboard_button = QPushButton(
            "Αρχική Σελίδα"
        )

        self.backup_button = QPushButton(
            "Backup"
        )

        self.restore_button = QPushButton(
            "Επαναφορά"
        )

        self.backups_button = QPushButton(
            "Ιστορικό Backup"
        )

        self.settings_button = QPushButton(
            "Ρυθμίσεις"
        )

        self.logs_button = QPushButton(
            "Καταγραφές"
        )

        self.about_button = QPushButton(
            "Πληροφορίες"
        )

        buttons = [

            self.dashboard_button,
            self.backup_button,
            self.restore_button,
            self.backups_button,
            self.settings_button,
            self.logs_button,
            self.about_button,

        ]

        for button in buttons:

            button.setMinimumHeight(
                BUTTON_HEIGHT
            )

            layout.addWidget(
                button
            )

        layout.addStretch()

        #
        # APPLICATION STATUS
        #

        self.status_title = QLabel(
            "Κατάσταση Agent"
        )

        self.status_label = QLabel(
            STATUS_READY
        )

        self.version_label = QLabel(
            f"v{APPLICATION_VERSION}"
        )

        self.status_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.version_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.status_title
        )

        layout.addWidget(
            self.status_label
        )

        layout.addWidget(
            self.version_label
        )

        self.setLayout(
            layout
        )

    def setup_styles(self):

        self.setStyleSheet(

            f"""

            QWidget {{

                background-color: {SIDEBAR_BACKGROUND};

            }}

            QPushButton {{

                background-color: {BUTTON_BACKGROUND};
                color: {WHITE_COLOR};

                border: 1px solid {BUTTON_BORDER_COLOR};
                border-radius: {BUTTON_BORDER_RADIUS}px;

                padding-left: 15px;

                font-size: {TEXT_FONT_SIZE}pt;
                text-align: left;

            }}

            QPushButton:hover {{

                background-color: {BUTTON_HOVER_BACKGROUND};

            }}

            """

        )

        self.title_label.setStyleSheet(

            f"""

            color: {GOLD_COLOR};

            font-size: 18pt;
            font-weight: bold;

            """

        )

        self.subtitle_label.setStyleSheet(

            f"""

            color: {WHITE_COLOR};

            font-size: 11pt;

            """

        )

        self.status_title.setStyleSheet(

            f"""

            color: {SECONDARY_TEXT_COLOR};

            font-size: 10pt;

            """

        )

        self.status_label.setStyleSheet(

            f"""

            color: {SUCCESS_COLOR};

            font-size: 12pt;
            font-weight: bold;

            """

        )

        self.version_label.setStyleSheet(

            f"""

            color: {SECONDARY_TEXT_COLOR};

            font-size: 9pt;

            """

        )