from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QDialog,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.common.status_chip import StatusChip
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

        self.setFixedHeight(
            48
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            15
        )

        #
        # LEFT
        #

        status = QLabel(
            "Everything is running normally."
        )

        status.setStyleSheet(
            """
            QLabel {
                color:#53C653;
                font-size:11pt;
                font-weight:600;
                background:transparent;
            }
            """
        )

        #
        # RIGHT
        #

        right = QHBoxLayout()

        right.setSpacing(
            12
        )

        #
        # DATABASE
        #

        self.database_button = QPushButton(
            "Database: Not Selected"
        )

        self.database_button.setCursor(
            Qt.PointingHandCursor
        )

        self.database_button.setFixedHeight(
            36
        )

        self.database_button.setStyleSheet(
            """
            QPushButton {
                background:#292b30;
                color:#ffffff;
                border:1px solid #3a3d43;
                border-radius:9px;
                padding:0 14px;
                font-size:9pt;
                font-weight:600;
            }

            QPushButton:hover {
                background:#33363c;
                border:1px solid #555a63;
            }
            """
        )

        self.database_button.clicked.connect(
            self.open_database_selector
        )

        #
        # CONNECTION
        #

        self.connected = StatusChip(
            "Not Connected",
            "warning",
        )

        #
        # SETTINGS
        #

        settings = QPushButton(
            "⚙"
        )

        settings.setCursor(
            Qt.PointingHandCursor
        )

        settings.setFixedSize(
            42,
            42
        )

        settings.setStyleSheet(
            f"""
            QPushButton {{
                background:{Theme.Colors.PRIMARY};
                color:white;
                border:none;
                border-radius:10px;
                font-size:16pt;
                font-weight:bold;
            }}

            QPushButton:hover {{
                background:#ff4b4b;
            }}
            """
        )

        #
        # ADD RIGHT SIDE
        #

        right.addWidget(
            self.database_button
        )

        right.addWidget(
            self.connected
        )

        right.addWidget(
            settings
        )

        #
        # MAIN LAYOUT
        #

        layout.addWidget(
            status
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
        database
    ):

        if not database:

            self.database_button.setText(
                "Database: Not Selected"
            )

            self.connected.setText(
                "Not Connected"
            )

            return

        database_name = (
            database.get("name")
            or "Unknown"
        )

        self.database_button.setText(
            f"Database: {database_name}"
        )

        self.connected.setText(
            "Connected"
        )