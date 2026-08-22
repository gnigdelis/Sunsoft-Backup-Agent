from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
    QWidget,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.cards.base_card import BaseCard


class ProgressCard(BaseCard):

    def __init__(self):

        super().__init__(
            title="Backup Progress",
            minimum_height=250,
        )

        self.build()

    #
    # Helpers
    #

    def create_caption(self, text):

        lbl = QLabel(text)

        lbl.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:9pt;
            """
        )

        return lbl

    def create_value(self, text, color=None):

        lbl = QLabel(text)

        lbl.setAlignment(
            Qt.AlignmentFlag.AlignRight |
            Qt.AlignmentFlag.AlignVCenter
        )

        lbl.setStyleSheet(
            f"""
            color:{color or Theme.Colors.TEXT};
            font-size:11pt;
            font-weight:600;
            """
        )

        return lbl

    def stat_row(self, title, value, color=None):

        row = QHBoxLayout()

        row.setContentsMargins(0, 0, 0, 0)

        row.addWidget(
            self.create_caption(title)
        )

        row.addStretch()

        row.addWidget(
            self.create_value(
                value,
                color,
            )
        )

        return row

    #
    # UI
    #

    def build(self):

        self.content_layout.setSpacing(10)

        #
        # Percentage
        #

        percent = QLabel("68%")

        percent.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        percent.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:28pt;
            font-weight:700;
            """
        )

        self.content_layout.addWidget(percent)

        #
        # Progress Bar
        #

        progress = QProgressBar()

        progress.setRange(0, 100)
        progress.setValue(68)
        progress.setTextVisible(False)
        progress.setFixedHeight(10)

        progress.setStyleSheet(
            f"""
            QProgressBar
            {{
                background:{Theme.Colors.BORDER};
                border:none;
                border-radius:5px;
            }}

            QProgressBar::chunk
            {{
                background:{Theme.Colors.PRIMARY};
                border-radius:5px;
            }}
            """
        )

        self.content_layout.addWidget(progress)

        self.content_layout.addSpacing(8)

        #
        # Statistics
        #

        stats = QWidget()

        stats_layout = QVBoxLayout(stats)

        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(8)

        stats_layout.addLayout(
            self.stat_row(
                "Files",
                "184,392 / 265,100",
            )
        )

        stats_layout.addLayout(
            self.stat_row(
                "Speed",
                "126 MB/s",
            )
        )

        stats_layout.addLayout(
            self.stat_row(
                "Remaining",
                "02:14",
            )
        )

        stats_layout.addLayout(
            self.stat_row(
                "Copied",
                "412 GB",
                Theme.Colors.SUCCESS,
            )
        )

        self.content_layout.addWidget(stats)

        #
        # Divider
        #

        divider = QFrame()

        divider.setFrameShape(
            QFrame.Shape.HLine
        )

        divider.setStyleSheet(
            f"""
            color:{Theme.Colors.BORDER};
            background:{Theme.Colors.BORDER};
            """
        )

        self.content_layout.addSpacing(8)
        self.content_layout.addWidget(divider)
        self.content_layout.addSpacing(8)

        #
        # Current Task
        #

        task_title = QLabel("Current Task")

        task_title.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:9pt;
            """
        )

        task_value = QLabel(
            "Compressing database backup..."
        )

        task_value.setWordWrap(True)

        task_value.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:11pt;
            font-weight:600;
            """
        )

        self.content_layout.addWidget(task_title)
        self.content_layout.addWidget(task_value)

        self.content_layout.addStretch()