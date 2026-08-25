from PySide6.QtWidgets import (
    QLabel,
    QGridLayout,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.cards.base_card import BaseCard


class StatisticsCard(BaseCard):

    def __init__(self):
        super().__init__(
            title="Backup Statistics",
            minimum_height=150,
        )

        self.build()

    def build(self):

        self.content_layout.setSpacing(
            10
        )

        # ======================================================
        # ORANGE ACCENT
        # ======================================================

        accent = QLabel()

        accent.setFixedHeight(
            3
        )

        accent.setStyleSheet(
            """
            QLabel {
                background: #FF9800;
                border: none;
                border-radius: 1px;
            }
            """
        )

        self.content_layout.insertWidget(
            0,
            accent
        )

        # ======================================================
        # STATISTICS
        # ======================================================

        grid = QGridLayout()

        grid.setContentsMargins(
            0,
            4,
            0,
            0
        )

        grid.setHorizontalSpacing(
            30
        )

        grid.setVerticalSpacing(
            10
        )

        self.files = self._value(
            "0"
        )

        self.size = self._value(
            "0 MB"
        )

        self.duration = self._value(
            "00:00"
        )

        self.compression = self._value(
            "0 %"
        )

        rows = [
            ("Files", self.files),
            ("Backup Size", self.size),
            ("Duration", self.duration),
            ("Compression", self.compression),
        ]

        for row, (
            title,
            value
        ) in enumerate(rows):

            label = QLabel(
                title
            )

            label.setStyleSheet(
                f"""
                QLabel {{
                    color:{Theme.Colors.TEXT_SECONDARY};
                    font-size:8.5pt;
                    font-weight:600;
                }}
                """
            )

            grid.addWidget(
                label,
                row,
                0
            )

            grid.addWidget(
                value,
                row,
                1
            )

        self.content_layout.addLayout(
            grid
        )

        self.content_layout.addStretch()

    def _value(
        self,
        value
    ):

        label = QLabel(
            value
        )

        label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:10pt;
                font-weight:700;
            }}
            """
        )

        return label

    def set_statistics(
        self,
        files: int,
        size: str,
        duration: str,
        compression: str,
    ):

        self.files.setText(
            str(files)
        )

        self.size.setText(
            size
        )

        self.duration.setText(
            duration
        )

        self.compression.setText(
            compression
        )