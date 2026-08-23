from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from core.discovery.system_discovery import SystemDiscovery
from core.controllers.backup_controller import BackupController

from ui.v2.widgets.cards.info_card import InfoCard
from ui.v2.widgets.cards.last_backup_card import LastBackupCard
from ui.v2.widgets.progress.progress_card import ProgressCard


class SummarySection(QWidget):

    def __init__(self):

        super().__init__()

        self.system = SystemDiscovery()

        self.system_info = self.system.discover()["data"]

        # -------------------------------------------------
        # Shared Backup Controller
        # -------------------------------------------------

        self.controller = BackupController()

        # -------------------------------------------------
        # UI
        # -------------------------------------------------

        self.setup_ui()

        # -------------------------------------------------
        # Signals
        # -------------------------------------------------

        self.connect_signals()

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):

        layout = QGridLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(15)

        #
        # Proportions
        #

        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 3)

        #
        # Storage
        #

        total = float(
            self.system_info["total_disk"].replace(
                " GB",
                "",
            )
        )

        free = float(
            self.system_info["free_disk"].replace(
                " GB",
                "",
            )
        )

        used = round(
            total - free,
            2,
        )

        percent = round(
            (used / total) * 100
        )

        #
        # FIRST ROW
        #

        layout.addWidget(

            InfoCard(

                title="Computer",

                lines=[

                    self.system_info[
                        "computer_name"
                    ],

                    self.system_info[
                        "windows_version"
                    ],

                    "Domain: (Coming Soon)",

                ],

                status="success",

            ),

            0,
            0,

        )

        layout.addWidget(

            InfoCard(

                title="Database",

                lines=[

                    "SQL Server",

                    "Connected",

                ],

                status="info",

            ),

            0,
            1,

        )

        layout.addWidget(

            InfoCard(

                title="Storage",

                lines=[

                    f"{used:.2f} GB Used",

                    f"{total:.2f} GB Total",

                    f"{percent}% Used",

                ],

                status="warning",

            ),

            0,
            2,

        )

        #
        # SECOND ROW
        #

        self.last_backup = LastBackupCard()

        self.progress = ProgressCard()

        layout.addWidget(

            self.last_backup,

            1,
            0,
            1,
            2,

        )

        layout.addWidget(

            self.progress,

            1,
            2,

        )

        #
        # Minimum sizes
        #

        self.last_backup.setMinimumWidth(
            700
        )

        self.progress.setMinimumWidth(
            430
        )

        self.setLayout(
            layout
        )

    # =====================================================
    # SIGNALS
    # =====================================================

    def connect_signals(self):

        #
        # Backup Progress
        #

        self.controller.progress_changed.connect(
            self.on_progress_changed
        )

        #
        # Backup Finished
        #

        self.controller.finished.connect(
            self.on_backup_finished
        )

    # =====================================================
    # BACKUP EVENTS
    # =====================================================

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

    def on_backup_finished(
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

            self.last_backup.update_backup()

        else:

            self.last_backup.set_failed()

    # =====================================================
    # RESET
    # =====================================================

    def reset_progress(self):

        self.progress.reset()