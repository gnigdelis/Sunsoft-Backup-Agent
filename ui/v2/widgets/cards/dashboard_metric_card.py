from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.widgets.common.svg_icon import SvgIcon


class DashboardMetricCard(BaseCard):

    def __init__(
        self,
        title: str,
        value: str,
        subtitle: str,
        icon: str,
        right_icon: str = "",
        accent: str = Theme.Colors.INFO,
        minimum_height: int = 175,
        success: bool = False,
    ):

        self.title_text = title
        self.value_text = value
        self.subtitle_text = subtitle

        self.icon_path = icon
        self.right_icon_path = right_icon

        self.accent = accent
        self.success = success

        super().__init__(
            title="",
            minimum_height=minimum_height,
        )

        self.build_card()

    # ==========================================================
    # UI
    # ==========================================================

    def build_card(self):

        self.content_layout.setContentsMargins(
            2,
            2,
            2,
            2,
        )

        self.content_layout.setSpacing(
            0
        )

        #
        # Accent line
        #

        accent_line = QFrame()

        accent_line.setFixedHeight(
            3
        )

        accent_line.setStyleSheet(
            f"""
            QFrame {{
                background:{self.accent};
                border:none;
                border-radius:2px;
            }}
            """
        )

        self.content_layout.addWidget(
            accent_line
        )

        self.content_layout.addSpacing(
            12
        )

        #
        # Header
        #

        header = QHBoxLayout()

        header.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        header.setSpacing(
            9
        )

        #
        # Neutral icon container
        #

        icon_container = QFrame()

        icon_container.setFixedSize(
            30,
            30,
        )

        icon_container.setStyleSheet(
            """
            QFrame {
                background: transparent;
                border: none;
            }
            """
        )

        icon_layout = QHBoxLayout(
            icon_container
        )

        icon_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        icon_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.icon_widget = SvgIcon(
            self.icon_path,
            size=20,
        )

        icon_layout.addWidget(
            self.icon_widget
        )

        header.addWidget(
            icon_container
        )

        #
        # Title
        #

        self.title_label = QLabel(
            self.title_text
        )

        self.title_label.setStyleSheet(
            f"""
            QLabel {{
                background:transparent;
                color:{Theme.Colors.TEXT};
                font-size:10.5pt;
                font-weight:700;
            }}
            """
        )

        header.addWidget(
            self.title_label
        )

        header.addStretch()

        self.content_layout.addLayout(
            header
        )

        self.content_layout.addSpacing(
            10
        )

        #
        # Value
        #

        self.value_label = QLabel(
            self.value_text
        )

        self.value_label.setStyleSheet(
            f"""
            QLabel {{
                background:transparent;
                color:{Theme.Colors.TEXT};
                font-size:17pt;
                font-weight:700;
            }}
            """
        )

        self.value_label.setWordWrap(
            False
        )

        self.content_layout.addWidget(
            self.value_label
        )

        self.content_layout.addSpacing(
            3
        )

        #
        # Subtitle
        #

        self.subtitle_label = QLabel(
            self.subtitle_text
        )

        self.subtitle_label.setStyleSheet(
            f"""
            QLabel {{
                background:transparent;
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
                font-weight:400;
            }}
            """
        )

        self.subtitle_label.setWordWrap(
            False
        )

        self.content_layout.addWidget(
            self.subtitle_label
        )

        #
        # Success badge
        #

        if self.success:

            self.content_layout.addSpacing(
                9
            )

            self.success_badge = QFrame()

            self.success_badge.setFixedHeight(
                25
            )

            self.success_badge.setStyleSheet(
                f"""
                QFrame {{
                    background:{Theme.Colors.SUCCESS};
                    border:none;
                    border-radius:12px;
                }}
                """
            )

            badge_layout = QHBoxLayout(
                self.success_badge
            )

            badge_layout.setContentsMargins(
                10,
                0,
                10,
                0,
            )

            badge_layout.setSpacing(
                5
            )

            check = QLabel(
                "✓"
            )

            check.setStyleSheet(
                """
                QLabel {
                    background:transparent;
                    color:white;
                    font-size:9pt;
                    font-weight:700;
                }
                """
            )

            text = QLabel(
                "SUCCESS"
            )

            text.setStyleSheet(
                """
                QLabel {
                    background:transparent;
                    color:white;
                    font-size:8pt;
                    font-weight:700;
                }
                """
            )

            badge_layout.addWidget(
                check
            )

            badge_layout.addWidget(
                text
            )

            self.content_layout.addWidget(
                self.success_badge,
                0,
                Qt.AlignmentFlag.AlignLeft,
            )

        self.content_layout.addStretch()

    # ==========================================================
    # UPDATE
    # ==========================================================

    def set_value(
        self,
        value: str,
    ):

        self.value_label.setText(
            str(value)
        )

    def set_subtitle(
        self,
        subtitle: str,
    ):

        self.subtitle_label.setText(
            str(subtitle)
        )

    # ==========================================================
    # SUCCESS
    # ==========================================================

    def set_success(
        self,
        value: bool,
    ):

        if value:

            if hasattr(
                self,
                "success_badge",
            ):

                self.success_badge.show()

            return

        if hasattr(
            self,
            "success_badge",
        ):

            self.success_badge.hide()