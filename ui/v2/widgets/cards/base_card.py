from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)

from ui.v2.styles.theme import Theme


class BaseCard(QFrame):

    def __init__(
        self,
        title: str,
        minimum_height: int = 180,
        icon: str = "",
    ):

        super().__init__()

        self.title = title
        self.icon = icon

        self.setMinimumHeight(minimum_height)

        self.setup_ui()

    def setup_ui(self):

        self.setObjectName("card")

        self.setStyleSheet(
            f"""
            QFrame#card {{
                background: {Theme.Colors.SURFACE};
                border: 1px solid {Theme.Colors.BORDER};
                border-radius: {Theme.Radius.MEDIUM}px;
            }}

            QLabel {{
                background: transparent;
                border: none;
            }}
            """
        )

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            Theme.Spacing.MD,
            Theme.Spacing.MD,
            Theme.Spacing.MD,
            Theme.Spacing.MD,
        )

        self.main_layout.setSpacing(
            Theme.Spacing.SM
        )

        #
        # HEADER
        #

        header = QHBoxLayout()

        if self.icon:

            self.icon_label = QLabel(
                self.icon
            )

            self.icon_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.icon_label.setFixedSize(
                40,
                40,
            )

            header.addWidget(
                self.icon_label
            )

            header.addSpacing(
                Theme.Spacing.SM
            )

        self.title_label = QLabel(
            self.title
        )

        self.title_label.setFont(
            Theme.Typography.heading()
        )

        self.title_label.setStyleSheet(
            f"""
            color: {Theme.Colors.TEXT};
            """
        )

        header.addWidget(
            self.title_label
        )

        header.addStretch()

        self.main_layout.addLayout(
            header
        )

        #
        # CONTENT
        #

        self.content_layout = QVBoxLayout()

        self.content_layout.setSpacing(
            Theme.Spacing.SM
        )

        self.main_layout.addLayout(
            self.content_layout
        )

        self.main_layout.addStretch()

    def add_widget(
        self,
        widget,
    ):

        self.content_layout.addWidget(
            widget
        )

    def add_layout(
        self,
        layout,
    ):

        self.content_layout.addLayout(
            layout
        )