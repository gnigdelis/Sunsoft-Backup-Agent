from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QProgressBar,
    QWidget,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.cards.base_card import BaseCard


class ProgressCard(BaseCard):

    def __init__(self):
        super().__init__(
            title="Backup Progress",
            minimum_height=220,
        )

        self.build()

    def build(self):

        self.content_layout.setSpacing(10)

        # ======================================================
        # RED ACCENT
        # ======================================================

        accent = QLabel()

        accent.setFixedHeight(
            3
        )

        accent.setStyleSheet(
            """
            QLabel {
                background: #E53935;
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
        # PERCENTAGE
        # ======================================================

        header = QHBoxLayout()

        header.setContentsMargins(
            0,
            0,
            0,
            0
        )

        percent_title = QLabel(
            "Progress"
        )

        percent_title.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        self.percent = QLabel(
            "0%"
        )

        self.percent.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.percent.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:11pt;
                font-weight:700;
            }}
            """
        )

        header.addWidget(
            percent_title
        )

        header.addStretch()

        header.addWidget(
            self.percent
        )

        self.content_layout.addLayout(
            header
        )

        # ======================================================
        # PROGRESS BAR
        # ======================================================

        self.progress = QProgressBar()

        self.progress.setRange(
            0,
            100
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
            QProgressBar {{
                background:{Theme.Colors.BORDER};
                border:none;
                border-radius:5px;
            }}

            QProgressBar::chunk {{
                background:{Theme.Colors.PRIMARY};
                border-radius:5px;
            }}
            """
        )

        self.content_layout.addWidget(
            self.progress
        )

        # ======================================================
        # STATISTICS
        # ======================================================

        stats = QWidget()

        stats_layout = QHBoxLayout(
            stats
        )

        stats_layout.setContentsMargins(
            0,
            4,
            0,
            4
        )

        stats_layout.setSpacing(
            18
        )

        self.steps_value = self._value(
            "Step 0 / 0"
        )

        self.speed_value = self._value(
            "0 MB/s"
        )

        self.remaining_value = self._value(
            "--:--"
        )

        self.copied_value = self._value(
            "0 MB"
        )

        stats_layout.addWidget(
            self._stat(
                "Steps",
                self.steps_value
            )
        )

        stats_layout.addWidget(
            self._stat(
                "Speed",
                self.speed_value
            )
        )

        stats_layout.addWidget(
            self._stat(
                "Remaining",
                self.remaining_value
            )
        )

        stats_layout.addWidget(
            self._stat(
                "Copied",
                self.copied_value
            )
        )

        self.content_layout.addWidget(
            stats
        )

        # ======================================================
        # CURRENT TASK
        # ======================================================

        task_title = QLabel(
            "Current Task"
        )

        task_title.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        self.task_value = QLabel(
            "Waiting..."
        )

        self.task_value.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:10pt;
                font-weight:600;
            }}
            """
        )

        self.task_value.setWordWrap(
            True
        )

        self.content_layout.addWidget(
            task_title
        )

        self.content_layout.addWidget(
            self.task_value
        )

    def _value(
        self,
        text
    ):

        label = QLabel(
            text
        )

        label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:9pt;
                font-weight:700;
            }}
            """
        )

        return label

    def _stat(
        self,
        title,
        value
    ):

        widget = QWidget()

        layout = QVBoxLayout(
            widget
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            2
        )

        label = QLabel(
            title
        )

        label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:8pt;
            }}
            """
        )

        layout.addWidget(
            label
        )

        layout.addWidget(
            value
        )

        return widget

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

        self.steps_value.setText(
            f"Step {current_step} / {total_steps}"
        )

        self.task_value.setText(
            task
        )

    def reset(self):

        self.percent.setText(
            "0%"
        )

        self.progress.setValue(
            0
        )

        self.steps_value.setText(
            "Step 0 / 0"
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

    def finish(
        self,
        success=True
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