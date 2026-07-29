from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QFrame,
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

    def create_title(self, text):

        label = QLabel(text)

        label.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:10pt;
            """
        )

        return label

    def create_value(self, text, color=None):

        label = QLabel(text)

        label.setStyleSheet(
            f"""
            color:{color or Theme.Colors.TEXT};
            font-size:12pt;
            font-weight:600;
            """
        )

        return label

    def build(self):

        self.content_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        #
        # Main Horizontal Layout
        #

        row = QHBoxLayout()

        row.setSpacing(25)

        #
        # Circular Progress
        #

        progress = CircularProgress(68)

        row.addWidget(
            progress,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        #
        # Right Panel
        #

        info = QVBoxLayout()

        info.setSpacing(8)

        #
        # Files
        #

        info.addWidget(
            self.create_title("Files")
        )

        info.addWidget(
            self.create_value("184,392 / 265,100")
        )

        #
        # Speed
        #

        info.addSpacing(6)

        info.addWidget(
            self.create_title("Speed")
        )

        info.addWidget(
            self.create_value("126 MB/s")
        )

        #
        # Remaining
        #

        info.addSpacing(6)

        info.addWidget(
            self.create_title("Remaining")
        )

        info.addWidget(
            self.create_value("02:14")
        )

        #
        # Copied
        #

        info.addSpacing(6)

        info.addWidget(
            self.create_title("Copied")
        )

        info.addWidget(
            self.create_value(
                "412 GB",
                Theme.Colors.PRIMARY,
            )
        )

        info.addStretch()

        row.addLayout(info)

        self.content_layout.addLayout(row)

        #
        # Divider
        #

        line = QFrame()

        line.setFrameShape(
            QFrame.Shape.HLine
        )

        line.setStyleSheet(
            """
            color:#353535;
            background:#353535;
            """
        )

        self.content_layout.addSpacing(10)
        self.content_layout.addWidget(line)
        self.content_layout.addSpacing(8)

        #
        # Current Task
        #

        task_title = QLabel("Current Task")

        task_title.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:10pt;
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