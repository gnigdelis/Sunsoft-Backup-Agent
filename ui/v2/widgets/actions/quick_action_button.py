from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.common.svg_icon import SvgIcon


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

        #
        # Icon Container
        #

        self.icon_container = QFrame()
        self.icon_container.setFixedSize(40, 40)

        icon_layout = QHBoxLayout(self.icon_container)
        icon_layout.setContentsMargins(8, 8, 8, 8)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon = SvgIcon(
            f"actions/{icon}",
            size=24,
        )

        icon_layout.addWidget(self.icon)

        self.icon_container.setStyleSheet(f"""
            QFrame {{
                background:{color};
                border-radius:8px;
            }}
        """)

        #
        # Title
        #

        self.title = QLabel(text)

        self.title.setStyleSheet(f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:11pt;
                font-weight:600;
                background:transparent;
            }}
        """)

        layout.addWidget(self.icon_container)
        layout.addWidget(self.title)
        layout.addStretch()

        self.setStyleSheet(f"""
            QFrame#QuickActionButton {{
                background:transparent;
                border-radius:12px;
            }}

            QFrame#QuickActionButton:hover {{
                background:{Theme.Colors.SURFACE_LIGHT};
            }}
        """)

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        super().mousePressEvent(event)