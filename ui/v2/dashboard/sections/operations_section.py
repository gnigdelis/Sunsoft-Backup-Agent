from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

from core.controllers.backup_controller import BackupController

from ui.v2.widgets.logs.live_activity_card import LiveActivityCard
from ui.v2.widgets.actions.quick_actions_card import QuickActionsCard


class OperationsSection(QWidget):

    def __init__(self):

        super().__init__()

        #
        # Controller
        #

        self.controller = BackupController()

        self.setup_ui()

        self.connect_signals()

    def setup_ui(self):

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(15)

        #
        # Left
        #

        self.live_activity = LiveActivityCard()

        #
        # Right
        #

        self.quick_actions = QuickActionsCard()

        layout.addWidget(
            self.live_activity,
            3,
        )

        layout.addWidget(
            self.quick_actions,
            1,
        )

        self.setLayout(layout)

    def connect_signals(self):

        #
        # Buttons
        #

        self.quick_actions.backup_clicked.connect(
            self.start_backup
        )

        #
        # Logs
        #

        self.controller.log_info.connect(
            self.on_info
        )

        self.controller.log_success.connect(
            self.on_success
        )

        self.controller.log_error.connect(
            self.on_error
        )

        self.controller.finished.connect(
            self.on_finished
        )

    def start_backup(self):

        self.live_activity.clear_logs()

        self.live_activity.add_log(
            "▶ Έναρξη Backup..."
        )

        self.controller.start_backup()

    def on_info(self, text):

        self.live_activity.add_log(
            f"ℹ {text}"
        )

    def on_success(self, text):

        self.live_activity.add_log(
            f"✔ {text}"
        )

    def on_error(self, text):

        self.live_activity.add_log(
            f"✖ {text}"
        )

    def on_finished(self, result):

        if result.get("success", False):

            self.live_activity.add_log(
                "✔ Το Backup ολοκληρώθηκε."
            )

        else:

            self.live_activity.add_log(
                "✖ Το Backup απέτυχε."
            )