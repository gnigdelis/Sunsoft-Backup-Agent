from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.common.svg_icon import SvgIcon


class NavigationItem(QFrame):

    clicked = Signal()

    def __init__(
        self,
        text: str,
        icon: str,
        color: str = Theme.Colors.PRIMARY,
        active: bool = False,
    ):
        super().__init__()

        self.active = active
        self.color = color

        self.setObjectName("NavigationItem")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(56)

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
            f"navigation/{icon}",
            size=24,
        )

        icon_layout.addWidget(self.icon)

        #
        # Title
        #

        self.title = QLabel(text)

        layout.addWidget(self.icon_container)
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

            self.icon_container.setStyleSheet("""
                QFrame {
                    background:rgba(255,255,255,0.18);
                    border-radius:8px;
                }
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

            self.icon_container.setStyleSheet(f"""
                QFrame {{
                    background:{self.color};
                    border-radius:8px;
                }}
            """)

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        super().mousePressEvent(event)