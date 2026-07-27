from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
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
        minimum_height: int = 180,
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
        # STATUS BAR
        #

        bar = QFrame()
        bar.setFixedHeight(5)

        bar.setStyleSheet(
            f"""
            background:{color};
            border:none;
            border-radius:2px;
            """
        )

        #
        # VALUE
        #

        valueLabel = QLabel(value)
        valueLabel.setFont(Theme.Typography.title())

        valueLabel.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:24pt;
            font-weight:700;
            """
        )

        #
        # SUBTITLE
        #

        subtitleLabel = QLabel(subtitle)

        subtitleLabel.setFont(
            Theme.Typography.body()
        )

        subtitleLabel.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            """
        )

        #
        # CONTENT
        #

        self.content_layout.addWidget(bar)
        self.content_layout.addSpacing(10)
        self.content_layout.addStretch()
        self.content_layout.addWidget(valueLabel)
        self.content_layout.addWidget(subtitleLabel)
        self.content_layout.addStretch()