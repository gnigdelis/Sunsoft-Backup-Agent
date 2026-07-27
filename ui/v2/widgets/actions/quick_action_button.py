from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
)

from ui.v2.styles.theme import Theme


class QuickActionButton(QFrame):

    clicked = Signal()

    def __init__(self, text: str, icon: str, color: str):
        super().__init__()

        self.setObjectName("QuickActionButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(54)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        self.icon = QLabel(icon)
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setFixedSize(34, 34)

        self.icon.setStyleSheet(f"""
            QLabel {{
                background: {color};
                color: white;
                border-radius: 8px;
                font-size: 14pt;
                font-weight: bold;
            }}
        """)

        self.title = QLabel(text)

        self.title.setStyleSheet(f"""
            QLabel {{
                color: {Theme.Colors.TEXT};
                font-size: 11pt;
                font-weight: 600;
                background: transparent;
            }}
        """)

        layout.addWidget(self.icon)
        layout.addWidget(self.title)
        layout.addStretch()

        self.setStyleSheet(f"""
            QFrame#QuickActionButton {{
                background: transparent;
                border-radius: 12px;
            }}

            QFrame#QuickActionButton:hover {{
                background: {Theme.Colors.SURFACE_LIGHT};
            }}
        """)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)