from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

from core.discovery.system_discovery import SystemDiscovery
from core.controllers.backup_controller import BackupController
from core.dashboard_data_provider import DashboardDataProvider
from core.destination_manager import DestinationManager
from core.database.database_context import database_context

from ui.v2.widgets.cards.info_card import InfoCard
from ui.v2.widgets.cards.last_backup_card import LastBackupCard
from ui.v2.widgets.progress.progress_card import ProgressCard
from ui.v2.styles.icons import Icons


class SummarySection(QWidget):

    def __init__(self):

        super().__init__()

        self.system = SystemDiscovery()

        self.system_info = (
            self.system.discover()["data"]
        )

        self.controller = BackupController()

        self.destination_manager = (
            DestinationManager()
        )

        self.setup_ui()

        self.connect_signals()

        self.refresh_summary()

        database_context.database_changed.connect(
            self.on_database_changed
        )

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            12
        )

        #
        # Last Backup
        #

        self.last_backup = (
            LastBackupCard()
        )

        #
        # Files
        #

        self.files_card = InfoCard(
            title="Files",
            lines=[
                "0",
                "Files in backup",
            ],
            status="info",
            icon=Icons.FILES,
            minimum_height=145,
        )

        #
        # Database
        #

        self.database_card = InfoCard(
            title="Database",
            lines=[
                "Not Connected",
                "SQL Server",
            ],
            status="warning",
            icon=Icons.DATABASE,
            minimum_height=145,
        )

        #
        # Backup Size
        #

        self.size_card = InfoCard(
            title="Backup Size",
            lines=[
                "0 MB",
                "Current backup size",
            ],
            status="info",
            icon=Icons.STORAGE,
            minimum_height=145,
        )

        #
        # Location
        #

        self.location_card = InfoCard(
            title="Location",
            lines=[
                "Not Configured",
                "Backup destination",
            ],
            status="warning",
            icon=Icons.STORAGE,
            minimum_height=145,
        )

        #
        # Add cards
        #

        layout.addWidget(
            self.last_backup,
            1,
        )

        layout.addWidget(
            self.files_card,
            1,
        )

        layout.addWidget(
            self.database_card,
            1,
        )

        layout.addWidget(
            self.size_card,
            1,
        )

        layout.addWidget(
            self.location_card,
            1,
        )

        self.setLayout(
            layout
        )

        #
        # Keep existing progress card
        # available for the backup controller.
        #

        self.progress = ProgressCard()

    # ==========================================================
    # SIGNALS
    # ==========================================================

    def connect_signals(self):

        self.controller.progress_changed.connect(
            self.on_progress_changed
        )

        self.controller.finished.connect(
            self.on_backup_finished
        )

    # ==========================================================
    # DATABASE
    # ==========================================================

    def on_database_changed(
        self,
        database,
    ):

        self.refresh_summary()

    # ==========================================================
    # REFRESH
    # ==========================================================

    def refresh_summary(self):

        #
        # Files
        #

        try:

            files = (
                DashboardDataProvider.get_backup_files()
            )

        except Exception:

            files = "0"

        if files is None:

            files = "0"

        files = str(
            files
        ).strip()

        if not files:

            files = "0"

        self.update_card(
            self.files_card,
            [
                files,
                "Files in backup",
            ],
        )

        #
        # Database
        #

        database = (
            database_context.active()
        )

        if database:

            database_status = "Connected"

            database_name = (
                database.get(
                    "name",
                    "SQL Server",
                )
                or "SQL Server"
            )

            database_state = "success"

        else:

            database_status = "Not Connected"
            database_name = "SQL Server"
            database_state = "warning"

        self.update_card(
            self.database_card,
            [
                database_status,
                database_name,
            ],
        )

        #
        # Backup Size
        #

        try:

            backup_size = (
                DashboardDataProvider.get_backup_size()
            )

        except Exception:

            backup_size = "0 MB"

        if not backup_size:

            backup_size = "0 MB"

        self.update_card(
            self.size_card,
            [
                str(backup_size),
                "Current backup size",
            ],
        )

        #
        # Location
        #

        try:

            result = (
                self.destination_manager
                .get_destination()
            )

            if result.get(
                "success",
                False,
            ):

                location = (
                    result["data"].get(
                        "destination_path"
                    )
                )

            else:

                location = None

        except Exception:

            location = None

        if not location:

            location = "Not Configured"

        self.update_card(
            self.location_card,
            [
                str(location),
                "Backup destination",
            ],
        )

    # ==========================================================
    # CARD UPDATE
    # ==========================================================

    def update_card(
        self,
        card,
        lines,
    ):

        #
        # Recreate the InfoCard because the
        # current InfoCard implementation does
        # not expose a content update method.
        #

        parent = (
            card.parentWidget()
        )

        if parent is None:

            return

        layout = (
            parent.layout()
        )

        if layout is None:

            return

        index = (
            layout.indexOf(card)
        )

        if index < 0:

            return

        if card is self.files_card:

            title = "Files"
            icon = Icons.FILES
            status = "info"

        elif card is self.database_card:

            title = "Database"

            icon = Icons.DATABASE

            status = (
                "success"
                if lines[0] == "Connected"
                else "warning"
            )

        elif card is self.size_card:

            title = "Backup Size"
            icon = Icons.STORAGE
            status = "info"

        else:

            title = "Location"
            icon = Icons.STORAGE

            status = (
                "success"
                if lines[0] != "Not Configured"
                else "warning"
            )

        new_card = InfoCard(
            title=title,
            lines=lines,
            status=status,
            icon=icon,
            minimum_height=145,
        )

        layout.insertWidget(
            index,
            new_card,
            1,
        )

        card.setParent(
            None
        )

        card.deleteLater()

        if card is self.files_card:

            self.files_card = (
                new_card
            )

        elif card is self.database_card:

            self.database_card = (
                new_card
            )

        elif card is self.size_card:

            self.size_card = (
                new_card
            )

        elif card is self.location_card:

            self.location_card = (
                new_card
            )

    # ==========================================================
    # BACKUP PROGRESS
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
    # BACKUP FINISHED
    # ==========================================================

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

        self.refresh_summary()

    # ==========================================================
    # RESET
    # ==========================================================

    def reset_progress(self):

        self.progress.reset()