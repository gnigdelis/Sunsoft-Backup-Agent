from pathlib import Path
import json
import os
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

from core.dashboard_data_provider import (
    DashboardDataProvider,
)

from core.destination_manager import (
    DestinationManager,
)

from core.database.database_context import (
    database_context,
)

from ui.v2.widgets.cards.dashboard_metric_card import (
    DashboardMetricCard,
)

from ui.v2.styles.icons import Icons
from ui.v2.styles.theme import Theme


class SummarySection(QWidget):

    STATE_DIRECTORY = (
        Path(
            os.environ.get(
                "LOCALAPPDATA",
                Path.home(),
            )
        )
        / "Sunsoft Backup Agent"
    )

    STATE_FILE = (
        STATE_DIRECTORY
        / "last_backup.json"
    )

    def __init__(self):

        super().__init__()

        self.destination_manager = (
            DestinationManager()
        )

        self.setup_ui()

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
            14
        )

        #
        # Last Backup
        #

        self.last_backup_card = (
            DashboardMetricCard(
                title="Last Backup",
                value="Never",
                subtitle="No backup recorded",
                icon=Icons.CLOCK,
                right_icon=Icons.CLOCK,
                accent="#8B3A3A",
                minimum_height=175,
                success=True,
            )
        )

        #
        # Files
        #

        self.files_card = (
            DashboardMetricCard(
                title="Files",
                value="0",
                subtitle="Total files backed up",
                icon=Icons.FILES,
                accent=Theme.Colors.INFO,
                minimum_height=175,
            )
        )

        #
        # Database
        #

        self.database_card = (
            DashboardMetricCard(
                title="Database",
                value="Not Connected",
                subtitle="SQL Server",
                icon=Icons.DATABASE,
                accent="#8E44AD",
                minimum_height=175,
            )
        )

        #
        # Backup Size
        #

        self.size_card = (
            DashboardMetricCard(
                title="Backup Size",
                value="0 MB",
                subtitle="Total backup size",
                icon=Icons.STORAGE,
                accent=Theme.Colors.WARNING,
                minimum_height=175,
            )
        )

        #
        # Location
        #

        self.location_card = (
            DashboardMetricCard(
                title="Location",
                value="Not Configured",
                subtitle="Primary destination",
                icon=Icons.STORAGE,
                accent=Theme.Colors.SUCCESS,
                minimum_height=175,
            )
        )

        #
        # Add cards
        #

        layout.addWidget(
            self.last_backup_card,
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

        self.refresh_last_backup()

        self.refresh_files()

        self.refresh_database()

        self.refresh_backup_size()

        self.refresh_location()

    # ==========================================================
    # LAST BACKUP
    # ==========================================================

    def refresh_last_backup(self):

        try:

            if not self.STATE_FILE.exists():

                self.last_backup_card.set_value(
                    "Never"
                )

                self.last_backup_card.set_subtitle(
                    "No backup recorded"
                )

                return

            with open(
                self.STATE_FILE,
                "r",
                encoding="utf-8",
            ) as state_file:

                data = json.load(
                    state_file
                )

            value = data.get(
                "last_backup"
            )

            if not value:

                self.last_backup_card.set_value(
                    "Never"
                )

                self.last_backup_card.set_subtitle(
                    "No backup recorded"
                )

                return

            backup_datetime = (
                datetime.fromisoformat(
                    value
                )
            )

            now = datetime.now()

            if (
                backup_datetime.date()
                == now.date()
            ):

                main_value = (
                    backup_datetime.strftime(
                        "Today %H:%M"
                    )
                )

            else:

                main_value = (
                    backup_datetime.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                )

            subtitle = (
                backup_datetime.strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
            )

            self.last_backup_card.set_value(
                main_value
            )

            self.last_backup_card.set_subtitle(
                subtitle
            )

        except Exception:

            self.last_backup_card.set_value(
                "Never"
            )

            self.last_backup_card.set_subtitle(
                "No backup recorded"
            )

    # ==========================================================
    # FILES
    # ==========================================================

    def refresh_files(self):

        try:

            files = (
                DashboardDataProvider
                .get_backup_files()
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

        self.files_card.set_value(
            files
        )

        self.files_card.set_subtitle(
            "Total files backed up"
        )

    # ==========================================================
    # DATABASE
    # ==========================================================

    def refresh_database(self):

        database = (
            database_context.active()
        )

        if database:

            self.database_card.set_value(
                "Connected"
            )

            self.database_card.set_subtitle(
                database.get(
                    "name",
                    "SQL Server",
                )
                or "SQL Server"
            )

        else:

            self.database_card.set_value(
                "Not Connected"
            )

            self.database_card.set_subtitle(
                "SQL Server"
            )

    # ==========================================================
    # BACKUP SIZE
    # ==========================================================

    def refresh_backup_size(self):

        try:

            size = (
                DashboardDataProvider
                .get_backup_size()
            )

        except Exception:

            size = "0 MB"

        if not size:

            size = "0 MB"

        self.size_card.set_value(
            str(size)
        )

        self.size_card.set_subtitle(
            "Total backup size"
        )

    # ==========================================================
    # LOCATION
    # ==========================================================

    def refresh_location(self):

        try:

            result = (
                self.destination_manager
                .get_destination()
            )

            if (
                result.get(
                    "success",
                    False,
                )
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

            self.location_card.set_value(
                "Not Configured"
            )

        else:

            self.location_card.set_value(
                str(location)
            )

        self.location_card.set_subtitle(
            "Primary destination"
        )