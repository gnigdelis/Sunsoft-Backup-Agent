from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from core.controllers.backup_controller import BackupController
from core.discovery.system_discovery import SystemDiscovery

from ui.v2.widgets.logs.live_activity_card import LiveActivityCard
from ui.v2.widgets.cards.info_card import InfoCard
from ui.v2.widgets.progress.progress_card import ProgressCard
from ui.v2.styles.icons import Icons


class OperationsSection(QWidget):

    def __init__(self):

        super().__init__()

        self.controller = BackupController()

        self.system = SystemDiscovery()

        self.system_info = (
            self.system.discover()["data"]
        )

        self.setup_ui()

        self.connect_signals()

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        main_layout = QHBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        main_layout.setSpacing(
            14
        )

        #
        # LEFT SIDE
        #

        left_layout = QVBoxLayout()

        left_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        left_layout.setSpacing(
            14
        )

        #
        # Live Backup Progress
        #

        self.progress = ProgressCard()

        self.progress.setMinimumHeight(
            245
        )

        self.progress.setMaximumHeight(
            275
        )

        left_layout.addWidget(
            self.progress,
            0,
        )

        #
        # Live Logs
        #

        self.live_activity = (
            LiveActivityCard()
        )

        left_layout.addWidget(
            self.live_activity,
            1,
        )

        #
        # RIGHT SIDE
        #

        self.system_card = InfoCard(
            title="System Information",
            lines=[
                self.system_info.get(
                    "computer_name",
                    "Unknown",
                ),
                self.system_info.get(
                    "windows_version",
                    "Unknown",
                ),
                "Sunsoft Support Agent v2.0",
                "Database connection available",
            ],
            status="info",
            icon=Icons.COMPUTER,
            minimum_height=530,
        )

        #
        # MAIN LAYOUT
        #

        main_layout.addLayout(
            left_layout,
            3,
        )

        main_layout.addWidget(
            self.system_card,
            1,
        )

        self.setLayout(
            main_layout
        )

    # ==========================================================
    # SIGNALS
    # ==========================================================

    def connect_signals(self):

        #
        # Backup Progress
        #

        self.controller.progress_changed.connect(
            self.on_progress_changed
        )

        #
        # Backup Logs
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

    # ==========================================================
    # PROGRESS
    # ==========================================================

    def on_progress_changed(
        self,
        percentage,
        current_step,
        total_steps,
        task,
    ):

        self.progress.update_progress(
            percentage,
            current_step,
            total_steps,
            task,
        )

    # ==========================================================
    # LOGS
    # ==========================================================

    def on_info(
        self,
        text,
    ):

        self.live_activity.add_log(
            f"INFO {text}"
        )

    def on_success(
        self,
        text,
    ):

        self.live_activity.add_log(
            f"SUCCESS {text}"
        )

    def on_error(
        self,
        text,
    ):

        self.live_activity.add_log(
            f"ERROR {text}"
        )

    # ==========================================================
    # FINISHED
    # ==========================================================

    def on_finished(
        self,
        result,
    ):

        success = result.get(
            "success",
            False,
        )

        self.progress.finish(
            success
        )

        if success:

            self.live_activity.add_log(
                "Backup Completed Successfully."
            )

        else:

            self.live_activity.add_log(
                "Backup Failed."
            )

    # ==========================================================
    # RESET
    # ==========================================================

    def reset_progress(self):

        self.progress.reset()