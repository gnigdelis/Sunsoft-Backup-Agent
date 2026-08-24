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

        self.setStyleSheet(
            """
            QFrame#NavigationItem {
                background: transparent;
                border: none;
                border-radius: 0px;
            }
            """
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
            color=Theme.Colors.TEXT,
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

        self.title.setStyleSheet(
            f"""
            QLabel {{
                background: transparent;
                border: none;
                color: {Theme.Colors.TEXT};
                font-size: 10.5pt;
                font-weight: 500;
            }}
            """
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

        normal_color = (
            Theme.Colors.TEXT
        )

        active_color = (
            Theme.Colors.PRIMARY
        )

        if self.active:

            self.title.setStyleSheet(
                f"""
                QLabel {{
                    background: transparent;
                    border: none;
                    color: {active_color};
                    font-size: 10.5pt;
                    font-weight: 700;
                }}
                """
            )

            self.icon.setColor(
                active_color
            )

        else:

            self.title.setStyleSheet(
                f"""
                QLabel {{
                    background: transparent;
                    border: none;
                    color: {normal_color};
                    font-size: 10.5pt;
                    font-weight: 500;
                }}
                """
            )

            self.icon.setColor(
                normal_color
            )

    # ==========================================================
    # MOUSE ENTER
    # ==========================================================

    def enterEvent(
        self,
        event,
    ):

        if not self.active:

            self.title.setStyleSheet(
                f"""
                QLabel {{
                    background: transparent;
                    border: none;
                    color: {Theme.Colors.PRIMARY};
                    font-size: 10.5pt;
                    font-weight: 500;
                }}
                """
            )

            self.icon.setColor(
                Theme.Colors.PRIMARY
            )

        super().enterEvent(
            event
        )

    # ==========================================================
    # MOUSE LEAVE
    # ==========================================================

    def leaveEvent(
        self,
        event,
    ):

        if not self.active:

            self.title.setStyleSheet(
                f"""
                QLabel {{
                    background: transparent;
                    border: none;
                    color: {Theme.Colors.TEXT};
                    font-size: 10.5pt;
                    font-weight: 500;
                }}
                """
            )

            self.icon.setColor(
                Theme.Colors.TEXT
            )

        super().leaveEvent(
            event
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