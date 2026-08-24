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

        self.setObjectName(
            "NavigationItem"
        )

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.setFixedHeight(
            50
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            10,
            5,
            10,
            5,
        )

        layout.setSpacing(
            12
        )

        #
        # Icon
        #

        self.icon = SvgIcon(
            icon
            if "/" in icon
            else f"navigation/{icon}",
            size=22,
        )

        layout.addWidget(
            self.icon
        )

        #
        # Title
        #

        self.title = QLabel(
            text
        )

        layout.addWidget(
            self.title
        )

        layout.addStretch()

        self.refresh()

    # ==========================================================
    # ACTIVE
    # ==========================================================

    def setActive(
        self,
        value: bool,
    ):

        self.active = value

        self.refresh()

    # ==========================================================
    # STYLE
    # ==========================================================

    def refresh(self):

        if self.active:

            self.setStyleSheet(
                f"""
                QFrame#NavigationItem {{
                    background:#1B2432;
                    border:none;
                    border-left:3px solid
                        {Theme.Colors.PRIMARY};
                    border-radius:7px;
                }}

                QLabel {{
                    background:transparent;
                    color:{Theme.Colors.PRIMARY};
                    font-size:10.5pt;
                    font-weight:700;
                }}
                """
            )

        else:

            self.setStyleSheet(
                f"""
                QFrame#NavigationItem {{
                    background:transparent;
                    border:none;
                    border-left:3px solid transparent;
                    border-radius:7px;
                }}

                QFrame#NavigationItem:hover {{
                    background:#17202D;
                    border-left:3px solid #334155;
                }}

                QLabel {{
                    background:transparent;
                    color:{Theme.Colors.TEXT};
                    font-size:10.5pt;
                    font-weight:500;
                }}
                """
            )

    # ==========================================================
    # CLICK
    # ==========================================================

    def mousePressEvent(
        self,
        event,
    ):

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):

            self.clicked.emit()

        super().mousePressEvent(
            event
        )