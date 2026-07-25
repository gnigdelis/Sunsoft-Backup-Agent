from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)


class ProgressWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        panel = PanelWidget(
            "Πρόοδος Backup"
        )

        panel_layout = QVBoxLayout()

        self.current_task = QLabel(
            "Αναμονή..."
        )

        self.progress = QProgressBar()

        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)

        self.step_label = QLabel(
            "Βήμα 0 από 0"
        )

        panel_layout.addWidget(
            self.current_task
        )

        panel_layout.addWidget(
            self.progress
        )

        panel_layout.addWidget(
            self.step_label
        )

        panel.add_layout(
            panel_layout
        )

        layout.addWidget(
            panel
        )

        self.setLayout(
            layout
        )

    def set_progress(
        self,
        value,
    ):

        self.progress.setValue(
            value
        )

    def set_task(
        self,
        task,
    ):

        self.current_task.setText(
            task
        )

    def set_step(
        self,
        current,
        total,
    ):

        self.step_label.setText(
            f"Βήμα {current} από {total}"
        )

    def reset(self):

        self.progress.setValue(0)

        self.current_task.setText(
            "Αναμονή..."
        )

        self.step_label.setText(
            "Βήμα 0 από 0"
        )