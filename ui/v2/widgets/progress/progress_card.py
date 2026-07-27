from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QGridLayout,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.widgets.progress.circular_progress import CircularProgress


class ProgressCard(BaseCard):

    def __init__(self):

        super().__init__(
            title="Backup Progress",
            minimum_height=220,
        )

        self.build()

    def build(self):

        progress = CircularProgress(68)

        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.content_layout.addWidget(
            progress,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        self.content_layout.addSpacing(10)

        grid = QGridLayout()

        grid.setHorizontalSpacing(25)
        grid.setVerticalSpacing(6)

        #
        # Files
        #

        files_title = QLabel("Files")
        files_title.setStyleSheet(
            f"color:{Theme.Colors.TEXT_SECONDARY};"
        )

        files_value = QLabel("184,392 / 265,100")
        files_value.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:11pt;
            font-weight:600;
            """
        )

        #
        # Speed
        #

        speed_title = QLabel("Speed")
        speed_title.setStyleSheet(
            f"color:{Theme.Colors.TEXT_SECONDARY};"
        )

        speed_value = QLabel("126 MB/s")
        speed_value.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:11pt;
            font-weight:600;
            """
        )

        #
        # Remaining
        #

        remain_title = QLabel("Remaining")
        remain_title.setStyleSheet(
            f"color:{Theme.Colors.TEXT_SECONDARY};"
        )

        remain_value = QLabel("02:14")
        remain_value.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:11pt;
            font-weight:600;
            """
        )

        #
        # Copied
        #

        copied_title = QLabel("Copied")
        copied_title.setStyleSheet(
            f"color:{Theme.Colors.TEXT_SECONDARY};"
        )

        copied_value = QLabel("412 GB")
        copied_value.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:11pt;
            font-weight:600;
            """
        )

        grid.addWidget(files_title, 0, 0)
        grid.addWidget(files_value, 1, 0)

        grid.addWidget(speed_title, 0, 1)
        grid.addWidget(speed_value, 1, 1)

        grid.addWidget(remain_title, 2, 0)
        grid.addWidget(remain_value, 3, 0)

        grid.addWidget(copied_title, 2, 1)
        grid.addWidget(copied_value, 3, 1)

        self.content_layout.addLayout(grid)
        self.content_layout.addStretch()