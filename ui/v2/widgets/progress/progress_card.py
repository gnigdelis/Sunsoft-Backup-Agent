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

    # =====================================================
    # HELPERS
    # =====================================================

    def create_caption(
        self,
        text,
    ):

        lbl = QLabel(
            text
        )

        lbl.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:10pt;
            """
        )

        return lbl

    def create_value(
        self,
        text,
        color=None,
    ):

        lbl = QLabel(
            text
        )

        lbl.setAlignment(
            Qt.AlignmentFlag.AlignRight |
            Qt.AlignmentFlag.AlignVCenter
        )

        lbl.setStyleSheet(
            f"""
            color:{color or Theme.Colors.TEXT};
            font-size:10pt;
            font-weight:600;
            """
        )

        return lbl

    def stat_row(
        self,
        title,
        value,
        color=None,
    ):

        row = QHBoxLayout()

        row.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        row.setSpacing(
            10
        )

        row.addWidget(
            self.create_caption(
                title
            )
        )

        row.addStretch()

        value_label = self.create_value(
            value,
            color,
        )

        row.addWidget(
            value_label
        )

        return row, value_label

    # =====================================================
    # UI
    # =====================================================

    def build(self):

        self.content_layout.setSpacing(
            8
        )

        #
        # Percentage
        #

        self.percent = QLabel(
            "0%"
        )

        self.percent.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.percent.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:28pt;
            font-weight:700;
            """
        )

        self.content_layout.addWidget(
            self.percent
        )

        #
        # Progress Bar
        #

        self.progress = QProgressBar()

        self.progress.setRange(
            0,
            100,
        )

        self.progress.setValue(
            0
        )

        self.progress.setTextVisible(
            False
        )

        self.progress.setFixedHeight(
            10
        )

        self.progress.setStyleSheet(
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

        self.content_layout.addWidget(
            self.progress
        )

        #
        # Statistics
        #

        stats = QWidget()

        stats_layout = QVBoxLayout(
            stats
        )

        stats_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        stats_layout.setSpacing(
            5
        )

        self.files_row, self.files_value = (
            self.stat_row(
                "Files",
                "0 / 0",
            )
        )

        self.speed_row, self.speed_value = (
            self.stat_row(
                "Speed",
                "0 MB/s",
            )
        )

        self.remaining_row, self.remaining_value = (
            self.stat_row(
                "Remaining",
                "--:--",
            )
        )

        self.copied_row, self.copied_value = (
            self.stat_row(
                "Copied",
                "0 MB",
                Theme.Colors.SUCCESS,
            )
        )

        stats_layout.addLayout(
            self.files_row
        )

        stats_layout.addLayout(
            self.speed_row
        )

        stats_layout.addLayout(
            self.remaining_row
        )

        stats_layout.addLayout(
            self.copied_row
        )

        self.content_layout.addWidget(
            stats
        )

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

        self.content_layout.addWidget(
            divider
        )

        #
        # Current Task
        #

        self.task_title = QLabel(
            "Current Task"
        )

        self.task_title.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:10pt;
            """
        )

        self.task_value = QLabel(
            "Waiting..."
        )

        self.task_value.setWordWrap(
            True
        )

        self.task_value.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:11pt;
            font-weight:600;
            """
        )

        self.content_layout.addWidget(
            self.task_title
        )

        self.content_layout.addWidget(
            self.task_value
        )

        self.content_layout.addStretch()

    # =====================================================
    # LIVE PROGRESS
    # =====================================================

    def update_progress(
        self,
        percentage,
        current_step,
        total_steps,
        task,
    ):

        self.percent.setText(
            f"{percentage}%"
        )

        self.progress.setValue(
            percentage
        )

        self.files_value.setText(
            f"Step {current_step} / {total_steps}"
        )

        self.task_value.setText(
            task
        )

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.percent.setText(
            "0%"
        )

        self.progress.setValue(
            0
        )

        self.files_value.setText(
            "0 / 0"
        )

        self.speed_value.setText(
            "0 MB/s"
        )

        self.remaining_value.setText(
            "--:--"
        )

        self.copied_value.setText(
            "0 MB"
        )

        self.task_value.setText(
            "Waiting..."
        )

    # =====================================================
    # FINISH
    # =====================================================

    def finish(
        self,
        success=True,
    ):

        if success:

            self.percent.setText(
                "100%"
            )

            self.progress.setValue(
                100
            )

            self.task_value.setText(
                "Backup Completed."
            )

        else:

            self.task_value.setText(
                "Backup Failed."
            )