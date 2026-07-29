from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
)

from ui.v2.styles.theme import Theme


class ProgressCard(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        self.title = QLabel("Backup Progress")
        self.title.setFont(
            Theme.Typography.heading()
        )
        self.title.setStyleSheet(
            f"color:{Theme.Colors.TEXT};"
        )

        self.percent = QLabel("0%")
        self.percent.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:11pt;
            """
        )

        self.task = QLabel("Waiting...")
        self.task.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:10pt;
            """
        )

        self.step = QLabel("Step 0 / 0")
        self.step.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:9pt;
            """
        )

        self.progress = QProgressBar()

        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(18)

        self.progress.setStyleSheet(
            f"""
            QProgressBar {{

                border: none;
                border-radius: 9px;
                background: {Theme.Colors.SURFACE_LIGHT};

            }}

            QProgressBar::chunk {{

                border-radius: 9px;
                background: #E53935;

            }}
            """
        )

        layout.addWidget(self.title)
        layout.addWidget(self.percent)
        layout.addWidget(self.progress)
        layout.addWidget(self.task)
        layout.addWidget(self.step)

        self.setStyleSheet(
            f"""
            ProgressCard {{

                background: {Theme.Colors.SURFACE};
                border: 1px solid {Theme.Colors.BORDER};
                border-radius: 12px;

            }}
            """
        )

    def update_progress(
        self,
        percentage,
        current_step,
        total_steps,
        current_task,
    ):

        percentage = max(
            0,
            min(100, percentage),
        )

        self.progress.setValue(
            percentage
        )

        self.percent.setText(
            f"{percentage}%"
        )

        self.task.setText(
            current_task
        )

        self.step.setText(
            f"Step {current_step} / {total_steps}"
        )

    def reset(self):

        self.update_progress(
            0,
            0,
            0,
            "Waiting...",
        )