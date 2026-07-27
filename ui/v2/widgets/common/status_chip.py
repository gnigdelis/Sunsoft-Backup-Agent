from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from ui.v2.styles.theme import Theme


class StatusChip(QLabel):

    COLORS = {
        "success": Theme.Colors.SUCCESS,
        "error": Theme.Colors.ERROR,
        "warning": Theme.Colors.WARNING,
        "info": Theme.Colors.INFO,
    }

    def __init__(self, text: str, status: str = "success", parent=None):
        super().__init__(text, parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(28)

        self.set_status(status)

    def set_status(self, status: str):

        color = self.COLORS.get(status, Theme.Colors.INFO)

        self.setStyleSheet(
            f"""
            QLabel {{
                background: {color};
                color: white;
                border-radius: 14px;
                padding-left: 12px;
                padding-right: 12px;
                font-size: 10pt;
                font-weight: 600;
            }}
            """
        )