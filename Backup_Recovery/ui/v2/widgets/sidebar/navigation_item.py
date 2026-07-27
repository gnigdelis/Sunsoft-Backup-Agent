from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
)

from ui.v2.styles.theme import Theme


class NavigationItem(QFrame):

    clicked = Signal()

    def __init__(
        self,
        text: str,
        icon: str = "",
        color: str = Theme.Colors.PRIMARY,
        active: bool = False,
    ):
        super().__init__()

        self.active = active
        self.color = color

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(56)
        self.setObjectName("NavigationItem")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        self.icon_box = QLabel(icon)
        self.icon_box.setAlignment(Qt.AlignCenter)
        self.icon_box.setFixedSize(34, 34)

        self.title = QLabel(text)

        layout.addWidget(self.icon_box)
        layout.addWidget(self.title)
        layout.addStretch()

        self.refresh()

    def setActive(self, value: bool):
        self.active = value
        self.refresh()

    def refresh(self):

        if self.active:

            self.setStyleSheet(f"""
                QFrame#NavigationItem {{
                    background:{Theme.Colors.PRIMARY};
                    border-radius:12px;
                }}

                QLabel {{
                    background:transparent;
                    color:white;
                    font-size:11pt;
                    font-weight:700;
                }}
            """)

            self.icon_box.setStyleSheet(f"""
                QLabel {{
                    background:rgba(255,255,255,0.18);
                    border-radius:8px;
                    color:white;
                    font-size:13pt;
                    font-weight:bold;
                }}
            """)

        else:

            self.setStyleSheet(f"""
                QFrame#NavigationItem {{
                    background:transparent;
                    border-radius:12px;
                }}

                QFrame#NavigationItem:hover {{
                    background:{Theme.Colors.SURFACE_LIGHT};
                }}

                QLabel {{
                    background:transparent;
                    color:{Theme.Colors.TEXT};
                    font-size:11pt;
                    font-weight:600;
                }}
            """)

            self.icon_box.setStyleSheet(f"""
                QLabel {{
                    background:{self.color};
                    border-radius:8px;
                    color:white;
                    font-size:13pt;
                    font-weight:bold;
                }}
            """)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)