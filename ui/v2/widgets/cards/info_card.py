from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QFrame, QWidget, QHBoxLayout

from ui.v2.styles.theme import Theme
from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.widgets.common.svg_icon import SvgIcon


class InfoCard(BaseCard):

    def __init__(
        self,
        title: str,
        lines: list[str],
        status: str = "info",
        icon: str | None = None,
        minimum_height: int = 160,
    ):

        super().__init__(
            title="",
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

        self.content_layout.addWidget(bar)
        self.content_layout.addSpacing(12)

        #
        # Header
        #

        header = QWidget()

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        if icon:

            header_layout.addWidget(
                SvgIcon(
                    icon,
                    size=22,
                )
            )

        title_label = QLabel(title)
        title_label.setFont(
            Theme.Typography.heading()
        )

        title_label.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-weight:700;
            """
        )

        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.content_layout.addWidget(header)
        self.content_layout.addSpacing(12)

        #
        # Information
        #

        for index, text in enumerate(lines):

            label = QLabel(text)

            if index == 0:

                label.setFont(
                    Theme.Typography.heading()
                )

                label.setStyleSheet(
                    f"""
                    color:{Theme.Colors.TEXT};
                    font-weight:700;
                    """
                )

            else:

                label.setFont(
                    Theme.Typography.body()
                )

                label.setStyleSheet(
                    f"""
                    color:{Theme.Colors.TEXT_SECONDARY};
                    """
                )

            label.setAlignment(
                Qt.AlignmentFlag.AlignLeft
            )

            self.content_layout.addWidget(label)
            self.content_layout.addSpacing(4)

        self.content_layout.addStretch()