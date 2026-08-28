from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)

from ui.v2.styles.theme import Theme


class Footer(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

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
            0
        )

        self.setStyleSheet(
            f"""
            QWidget {{
                background:transparent;
                border:none;
            }}

            QLabel {{
                background:transparent;
                border:none;
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        # ======================================================
        # BUILD
        # ======================================================

        self.version = QLabel(
            "Build 2.0.0"
        )

        layout.addStretch()

        layout.addWidget(
            self.version
        )

    # ==========================================================
    # DATABASE STATUS
    # ==========================================================

    def update_database_status(
        self,
        database,
    ):

        pass