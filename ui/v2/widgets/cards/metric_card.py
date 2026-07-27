from PySide6.QtWidgets import (
    QLabel,
    QFrame,
)

from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.styles.theme import Theme


class MetricCard(BaseCard):

    def __init__(
        self,
        title: str,
        value: str,
        subtitle: str = "",
        status: str = "info",
        minimum_height: int = 140,
    ):

        super().__init__(
            title=title,
            minimum_height=minimum_height,
        )

        colors = {
            "success": Theme.Colors.SUCCESS,
            "warning": Theme.Colors.WARNING,
            "error": Theme.Colors.ERROR,
            "info": Theme.Colors.INFO,
        }

        color = colors.get(status, Theme.Colors.INFO)

        #
        # Status Bar
        #

        bar = QFrame()
        bar.setFixedHeight(4)

        bar.setStyleSheet(
            f"""
            background:{color};
            border:none;
            border-radius:2px;
            """
        )

        #
        # Value
        #

        value_label = QLabel(value)

        value_label.setFont(
            Theme.Typography.title()
        )

        value_label.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:22pt;
            font-weight:700;
            """
        )

        #
        # Subtitle
        #

        subtitle_label = QLabel(subtitle)

        subtitle_label.setFont(
            Theme.Typography.body()
        )

        subtitle_label.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            """
        )

        #
        # Layout
        #

        self.content_layout.addWidget(bar)
        self.content_layout.addSpacing(8)

        self.content_layout.addWidget(value_label)

        self.content_layout.addSpacing(4)

        self.content_layout.addWidget(subtitle_label)

        self.content_layout.addStretch()