from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from ui.v2.styles.theme import Theme


class StatusWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            6
        )

        title = QLabel(
            "SYSTEM STATUS"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        title.setStyleSheet(
            f"""
            QLabel {{
                color: {Theme.Colors.TEXT_DISABLED};
                font-size: 9pt;
                font-weight: 600;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }}
            """
        )

        self.status = QLabel(
            "● READY"
        )

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.status.setStyleSheet(
            f"""
            QLabel {{
                color: {Theme.Colors.SUCCESS};
                font-size: 11pt;
                font-weight: 700;
                background: transparent;
                border: none;
            }}
            """
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            self.status
        )