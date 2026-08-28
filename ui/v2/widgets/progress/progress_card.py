import time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGridLayout,
)

from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.styles.theme import Theme


class CircularProgress(QWidget):

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(parent)

        self.value = 0

        self.setMinimumSize(
            150,
            150,
        )

    def setValue(
        self,
        value,
    ):

        self.value = max(
            0,
            min(
                100,
                int(value),
            ),
        )

        self.update()

    def paintEvent(
        self,
        event,
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        rect = self.rect().adjusted(
            12,
            12,
            -12,
            -12,
        )

        #
        # Background ring
        #

        background_pen = QPen(
            Theme.Colors.BORDER
        )

        background_pen.setWidth(
            12
        )

        background_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(
            background_pen
        )

        painter.drawArc(
            rect,
            90 * 16,
            -360 * 16,
        )

        #
        # Progress ring
        #

        progress_pen = QPen(
            Theme.Colors.PRIMARY
        )

        progress_pen.setWidth(
            12
        )

        progress_pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(
            progress_pen
        )

        span = int(
            -360
            * 16
            * self.value
            / 100
        )

        painter.drawArc(
            rect,
            90 * 16,
            span,
        )

        #
        # Percentage
        #

        painter.setPen(
            Theme.Colors.TEXT
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                22,
                QFont.Weight.Bold,
            )
        )

        painter.drawText(
            rect,
            Qt.AlignmentFlag.AlignCenter,
            f"{self.value}%",
        )

        #
        # Label
        #

        label_rect = rect.adjusted(
            0,
            38,
            0,
            38,
        )

        painter.setPen(
            Theme.Colors.TEXT_SECONDARY
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Normal,
            )
        )

        painter.drawText(
            label_rect,
            Qt.AlignmentFlag.AlignCenter,
            (
                "Completed"
                if self.value == 100
                else "Progress"
            ),
        )


class ProgressCard(BaseCard):

    def __init__(self):

        self._started_at = None

        super().__init__(
            title="Live Backup Progress",
            minimum_height=250,
        )

        self.build_progress_ui()

        self._elapsed_timer = QTimer(self)

        self._elapsed_timer.setInterval(
            1000
        )

        self._elapsed_timer.timeout.connect(
            self._update_elapsed
        )

    # ==========================================================
    # UI
    # ==========================================================

    def build_progress_ui(self):

        self.content_layout.setSpacing(
            10
        )

        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        main_layout.setSpacing(
            24
        )

        #
        # Circular progress
        #

        self.circular = CircularProgress()

        self.circular.setFixedSize(
            150,
            150,
        )

        main_layout.addWidget(
            self.circular,
            0,
            Qt.AlignmentFlag.AlignVCenter,
        )

        #
        # Center information
        #

        center_layout = QVBoxLayout()

        center_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        center_layout.setSpacing(
            6
        )

        self.status_title = QLabel(
            "Waiting for backup..."
        )

        self.status_title.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:15pt;
                font-weight:700;
                background:transparent;
            }}
            """
        )

        center_layout.addWidget(
            self.status_title
        )

        self.status_description = QLabel(
            "Backup process is ready."
        )

        self.status_description.setWordWrap(
            True
        )

        self.status_description.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:10pt;
                background:transparent;
            }}
            """
        )

        center_layout.addWidget(
            self.status_description
        )

        #
        # Steps
        #

        steps_container = QWidget()

        steps_layout = QGridLayout(
            steps_container
        )

        steps_layout.setContentsMargins(
            0,
            8,
            0,
            0,
        )

        steps_layout.setHorizontalSpacing(
            18
        )

        steps_layout.setVerticalSpacing(
            4
        )

        self.step_labels = []

        step_names = [
            "Preparing",
            "Files",
            "Database",
            "Compression",
            "Verify",
        ]

        for index, name in enumerate(
            step_names
        ):

            label = QLabel(
                f"● {name}"
            )

            label.setStyleSheet(
                f"""
                QLabel {{
                    color:{Theme.Colors.TEXT_SECONDARY};
                    font-size:9pt;
                    font-weight:600;
                    background:transparent;
                }}
                """
            )

            steps_layout.addWidget(
                label,
                0,
                index,
            )

            self.step_labels.append(
                label
            )

        center_layout.addWidget(
            steps_container
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
            QFrame {{
                color:{Theme.Colors.BORDER};
                background:{Theme.Colors.BORDER};
                border:none;
                max-height:1px;
            }}
            """
        )

        center_layout.addWidget(
            divider
        )

        #
        # Current task
        #

        task_row = QHBoxLayout()

        task_title = QLabel(
            "Current Task"
        )

        task_title.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
                background:transparent;
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
                background:transparent;
            }}
            """
        )

        task_row.addWidget(
            task_title
        )

        task_row.addStretch()

        task_row.addWidget(
            self.task_value
        )

        center_layout.addLayout(
            task_row
        )

        main_layout.addLayout(
            center_layout,
            1,
        )

        #
        # Right statistics
        #

        stats_frame = QFrame()

        stats_frame.setStyleSheet(
            f"""
            QFrame {{
                background:transparent;
                border:none;
            }}
            """
        )

        stats_layout = QVBoxLayout(
            stats_frame
        )

        stats_layout.setContentsMargins(
            18,
            0,
            0,
            0,
        )

        stats_layout.setSpacing(
            14
        )

        elapsed_title = QLabel(
            "Elapsed Time"
        )

        elapsed_title.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
                background:transparent;
            }}
            """
        )

        self.elapsed_value = QLabel(
            "00:00:00"
        )

        self.elapsed_value.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:11pt;
                font-weight:700;
                background:transparent;
            }}
            """
        )

        stats_layout.addWidget(
            elapsed_title
        )

        stats_layout.addWidget(
            self.elapsed_value
        )

        speed_title = QLabel(
            "Speed"
        )

        speed_title.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
                background:transparent;
            }}
            """
        )

        self.speed_value = QLabel(
            "--"
        )

        self.speed_value.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:11pt;
                font-weight:700;
                background:transparent;
            }}
            """
        )

        stats_layout.addWidget(
            speed_title
        )

        stats_layout.addWidget(
            self.speed_value
        )

        stats_layout.addStretch()

        main_layout.addWidget(
            stats_frame,
            0,
        )

        self.content_layout.addLayout(
            main_layout
        )

        #
        # Bottom progress line
        #

        self.progress_line = QFrame()

        self.progress_line.setFixedHeight(
            8
        )

        self.progress_line.setStyleSheet(
            f"""
            QFrame {{
                background:{Theme.Colors.BORDER};
                border:none;
                border-radius:4px;
            }}
            """
        )

        self.content_layout.addWidget(
            self.progress_line
        )

    # ==========================================================
    # STEPS
    # ==========================================================

    def update_steps(
        self,
        current_step,
        total_steps,
    ):

        if total_steps <= 0:
            return

        step_count = len(
            self.step_labels
        )

        for index, label in enumerate(
            self.step_labels
        ):

            step_number = index + 1

            if step_number < current_step:

                color = (
                    Theme.Colors.SUCCESS
                )

                prefix = "●"

            elif step_number == current_step:

                color = (
                    Theme.Colors.PRIMARY
                )

                prefix = "●"

            else:

                color = (
                    Theme.Colors.TEXT_SECONDARY
                )

                prefix = "○"

            text = label.text()

            if " " in text:

                name = text.split(
                    " ",
                    1,
                )[1]

            else:

                name = text

            label.setText(
                f"{prefix} {name}"
            )

            label.setStyleSheet(
                f"""
                QLabel {{
                    color:{color};
                    font-size:9pt;
                    font-weight:600;
                    background:transparent;
                }}
                """
            )

    # ==========================================================
    # LIVE PROGRESS
    # ==========================================================

    def _update_elapsed(self):

        if self._started_at is None:
            return

        elapsed = int(
            time.monotonic()
            - self._started_at
        )

        hours = elapsed // 3600

        minutes = (
            elapsed % 3600
        ) // 60

        seconds = elapsed % 60

        self.elapsed_value.setText(
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    def update_progress(
        self,
        percentage,
        current_step,
        total_steps,
        task,
    ):

        if self._started_at is None:

            self._started_at = time.monotonic()

            self._elapsed_timer.start()

        self.circular.setValue(
            percentage
        )

        self.update_steps(
            current_step,
            total_steps,
        )

        self.task_value.setText(
            task
            if task
            else "Working..."
        )

        self.status_title.setText(
            "Backup in progress..."
        )

        self.status_description.setText(
            "The backup process is currently running."
        )

        self.speed_value.setText(
            "--"
        )

        progress_style = f"""
            QFrame {{
                background:qlineargradient(
                    x1:0,
                    y1:0,
                    x2:1,
                    y2:0,
                    stop:0 {Theme.Colors.PRIMARY},
                    stop:{max(0.0, min(1.0, percentage / 100))} {Theme.Colors.PRIMARY},
                    stop:{max(0.0, min(1.0, percentage / 100))} {Theme.Colors.BORDER},
                    stop:1 {Theme.Colors.BORDER}
                );
                border:none;
                border-radius:4px;
            }}
        """

        self.progress_line.setStyleSheet(
            progress_style
        )

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):

        self._elapsed_timer.stop()

        self._started_at = None

        self.circular.setValue(
            0
        )

        self.task_value.setText(
            "Waiting..."
        )

        self.status_title.setText(
            "Waiting for backup..."
        )

        self.status_description.setText(
            "Backup process is ready."
        )

        self.elapsed_value.setText(
            "00:00:00"
        )

        self.speed_value.setText(
            "--"
        )

        for label in self.step_labels:

            name = label.text()

            if " " in name:

                name = name.split(
                    " ",
                    1,
                )[1]

            label.setText(
                f"○ {name}"
            )

            label.setStyleSheet(
                f"""
                QLabel {{
                    color:{Theme.Colors.TEXT_SECONDARY};
                    font-size:9pt;
                    font-weight:600;
                    background:transparent;
                }}
                """
            )

        self.progress_line.setStyleSheet(
            f"""
            QFrame {{
                background:{Theme.Colors.BORDER};
                border:none;
                border-radius:4px;
            }}
            """
        )

    # ==========================================================
    # FINISH
    # ==========================================================

    def finish(
        self,
        success=True,
    ):

        self._elapsed_timer.stop()

        if success:

            self.circular.setValue(
                100
            )

            self.status_title.setText(
                "Backup Completed Successfully"
            )

            self.status_description.setText(
                "All available backup tasks completed successfully."
            )

            self.task_value.setText(
                "Backup completed successfully."
            )

            self.elapsed_value.setText(
                self.elapsed_value.text()
            )

            self.speed_value.setText(
                "--"
            )

            for label in self.step_labels:

                label.setText(
                    "● "
                    + (
                        label.text().split(
                            " ",
                            1,
                        )[1]
                        if " " in label.text()
                        else label.text()
                    )
                )

                label.setStyleSheet(
                    f"""
                    QLabel {{
                        color:{Theme.Colors.SUCCESS};
                        font-size:9pt;
                        font-weight:600;
                        background:transparent;
                    }}
                    """
                )

            self.progress_line.setStyleSheet(
                f"""
                QFrame {{
                    background:{Theme.Colors.PRIMARY};
                    border:none;
                    border-radius:4px;
                }}
                """
            )

        else:

            self.status_title.setText(
                "Backup Failed"
            )

            self.status_description.setText(
                "The backup process did not complete successfully."
            )

            self.task_value.setText(
                "Backup failed."
            )

            self.speed_value.setText(
                "--"
            )