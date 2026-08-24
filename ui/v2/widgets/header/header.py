from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QDialog,
)

from ui.v2.styles.theme import Theme
from ui.v2.styles.icons import Icons
from ui.v2.widgets.common.status_chip import StatusChip
from ui.v2.widgets.common.svg_icon import SvgIcon
from ui.v2.widgets.header.database_selector import DatabaseSelector

from core.database.database_context import database_context


class Header(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.update_database_display(
            database_context.active()
        )

    def setup_ui(self):

        self.setFixedHeight(52)

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(10)

        #
        # Right side
        #

        right = QHBoxLayout()

        right.setSpacing(12)

        self.connected = StatusChip(
            "Not Connected",
            "warning",
        )

        #
        # Settings / UDL
        #

        self.settings_button = QPushButton()

        self.settings_button.setCursor(
            Qt.PointingHandCursor
        )

        self.settings_button.setFixedSize(
            42,
            42,
        )

        self.settings_button.setObjectName(
            "HeaderSettingsButton"
        )

        settings_layout = QHBoxLayout(
            self.settings_button
        )

        settings_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        settings_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        settings_icon = SvgIcon(
            Icons.SETTINGS,
            size=20,
        )

        settings_layout.addWidget(
            settings_icon
        )

        self.settings_button.setStyleSheet(
            f"""
            QPushButton#HeaderSettingsButton {{
                background:#172131;
                border:1px solid {Theme.Colors.BORDER};
                border-radius:10px;
            }}

            QPushButton#HeaderSettingsButton:hover {{
                background:#202D3F;
                border:1px solid {Theme.Colors.BORDER_LIGHT};
            }}

            QPushButton#HeaderSettingsButton:pressed {{
                background:#141D2A;
            }}
            """
        )

        self.settings_button.clicked.connect(
            self.open_database_selector
        )

        right.addWidget(
            self.connected
        )

        right.addWidget(
            self.settings_button
        )

        layout.addStretch()

        layout.addLayout(
            right
        )

        #
        # DATABASE CHANGE
        #

        database_context.database_changed.connect(
            self.update_database_display
        )

    def open_database_selector(self):

        dialog = DatabaseSelector(
            self
        )

        if dialog.exec() != QDialog.Accepted:
            return

        if not dialog.selected_udl:
            return

        database_context.select(
            dialog.selected_udl
        )

    def update_database_display(
        self,
        database,
    ):

        if not database:

            self.connected.setText(
                "Not Connected"
            )

            return

        self.connected.setText(
            "Connected"
        )
