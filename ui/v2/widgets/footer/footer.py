from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)

from ui.v2.styles.theme import Theme

from core.database.database_context import (
    database_context,
)


class Footer(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.update_database_status(
            database_context.active()
        )

        database_context.database_changed.connect(
            self.update_database_status
        )

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        self.setFixedHeight(
            42
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            10,
            0,
            10,
            0,
        )

        layout.setSpacing(
            18
        )

        self.setStyleSheet(
            f"""
            QWidget {{
                background:transparent;
                border-top:1px solid {Theme.Colors.BORDER};
            }}

            QLabel {{
                background:transparent;
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        #
        # Engine
        #

        self.engine = QLabel(
            "Engine : Ready"
        )

        #
        # Database
        #

        self.database = QLabel(
            "Database : Not Connected"
        )

        #
        # Provider
        #

        self.provider = QLabel(
            "Provider : Idle"
        )

        #
        # Build
        #

        self.version = QLabel(
            "Build 2.0.0"
        )

        #
        # Layout
        #

        layout.addWidget(
            self.engine
        )

        layout.addSpacing(
            20
        )

        layout.addWidget(
            self.database
        )

        layout.addSpacing(
            20
        )

        layout.addWidget(
            self.provider
        )

        layout.addStretch()

        layout.addWidget(
            self.version,
            alignment=Qt.AlignmentFlag.AlignRight,
        )

    # ==========================================================
    # DATABASE STATUS
    # ==========================================================

    def update_database_status(
        self,
        database,
    ):

        if database:

            self.database.setText(
                "Database : Connected"
            )

        else:

            self.database.setText(
                "Database : Not Connected"
            )