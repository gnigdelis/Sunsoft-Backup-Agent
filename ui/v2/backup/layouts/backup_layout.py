from pathlib import Path
import os
import socket

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)

from core.controllers.backup_controller import BackupController
from core.destination_manager import DestinationManager
from core.database.database_context import database_context

from ui.v2.styles.theme import Theme

from ui.v2.backup.widgets.backup_toolbar import BackupToolbar
from ui.v2.widgets.backup.progress_card import ProgressCard
from ui.v2.widgets.backup.customer_card import CustomerCard
from ui.v2.widgets.backup.statistics_card import StatisticsCard
from ui.v2.widgets.logs.live_activity_card import LiveActivityCard


class BackupLayout(QWidget):

    def __init__(self):

        super().__init__()

        self.backup_controller = BackupController()

        self.destination_manager = (
            DestinationManager()
        )

        self.setup_ui()

        self.connect_events()

        if database_context.is_selected():
            self._update_customer_information()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def setup_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        root.setSpacing(
            20
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = QHBoxLayout()

        title = QLabel(
            "Backup Manager"
        )

        title.setFont(
            Theme.Typography.title()
        )

        title.setStyleSheet(
            f"color:{Theme.Colors.TEXT};"
        )

        self.status = QLabel(
            "🟢 Έτοιμο"
        )

        self.status.setStyleSheet(
            f"color:{Theme.Colors.SUCCESS}; font-size:11pt;"
        )

        header.addWidget(
            title
        )

        header.addStretch()

        header.addWidget(
            self.status
        )

        # -----------------------------------------------------
        # Widgets
        # -----------------------------------------------------

        self.toolbar = BackupToolbar()

        self.progress_card = ProgressCard()

        self.customer_card = CustomerCard()

        self.activity_card = LiveActivityCard()

        self.statistics_card = StatisticsCard()

        # -----------------------------------------------------
        # Middle Area
        # -----------------------------------------------------

        middle = QHBoxLayout()

        middle.setSpacing(
            20
        )

        middle.addWidget(
            self.customer_card,
            1,
        )

        middle.addWidget(
            self.activity_card,
            2,
        )

        # -----------------------------------------------------
        # Build Layout
        # -----------------------------------------------------

        root.addLayout(
            header
        )

        root.addWidget(
            self.toolbar
        )

        root.addWidget(
            self.progress_card
        )

        root.addLayout(
            middle
        )

        root.addWidget(
            self.statistics_card
        )

        root.addStretch()

    # ---------------------------------------------------------
    # Events
    # ---------------------------------------------------------

    def connect_events(self):

        self.toolbar.start_backup.connect(
            self._start_backup
        )

        self.toolbar.browse_clicked.connect(
            self._browse_destination
        )

        self.toolbar.open_destination_clicked.connect(
            self._open_destination
        )

        self.backup_controller.progress_changed.connect(
            self.progress_card.update_progress
        )

        self.backup_controller.log_info.connect(
            self._log_info
        )

        self.backup_controller.log_success.connect(
            self._log_success
        )

        self.backup_controller.log_error.connect(
            self._log_error
        )

        self.backup_controller.finished.connect(
            self._backup_finished
        )

        database_context.database_changed.connect(
            self._on_database_changed
        )

    # ---------------------------------------------------------
    # Customer Information
    # ---------------------------------------------------------

    def _on_database_changed(
        self,
        database,
    ):

        self._update_customer_information()

    def _update_customer_information(self):

        database = database_context.active()

        if not database:
            return

        destination = "-"

        destination_result = (
            self.destination_manager
            .get_destination()
        )

        if destination_result["success"]:

            destination = (
                destination_result["data"]
                .get(
                    "destination_path",
                    "-"
                )
            )

        self.customer_card.set_customer(

            customer=socket.gethostname() or "-",

            sql_server=(
                database.get("server")
                or "-"
            ),

            database=(
                database.get("name")
                or "-"
            ),

            database_version="-",

            cloud="Not configured",

            destination=str(destination),

            last_backup="-",

            next_backup="-",
        )

    # ---------------------------------------------------------
    # Start Backup
    # ---------------------------------------------------------

    def _start_backup(self):

        if self.backup_controller.is_running:

            return

        result = (
            self.backup_controller.start_backup()
        )

        if not result["success"]:

            error_message = (
                result["errors"][0]
                if result["errors"]
                else "Unable to start backup."
            )

            self.activity_card.add_log(
                error_message
            )

            QMessageBox.warning(
                self,
                "Database Selection Required",
                error_message,
            )

            self.status.setText(
                "β— Database Required"
            )

            self.status.setStyleSheet(
                "color:#f59e0b; font-size:11pt;"
            )

            return

        self._update_customer_information()

        self.status.setText(
            "β— Backup Running"
        )

        self.status.setStyleSheet(
            "color:#f59e0b; font-size:11pt;"
        )

        self.activity_card.add_log(
            "Database selected. Backup starting..."
        )

    # ---------------------------------------------------------
    # Browse Destination
    # ---------------------------------------------------------

    def _browse_destination(self):

        result = (
            self.destination_manager
            .get_destination()
        )

        if result["success"]:

            current_path = (
                result["data"][
                    "destination_path"
                ]
            )

        else:

            current_path = str(
                Path.home()
            )

        if not current_path:

            current_path = str(
                Path.home()
            )

        selected_directory = (
            QFileDialog.getExistingDirectory(
                self,
                "Select Backup Destination",
                current_path,
                QFileDialog.Option.ShowDirsOnly,
            )
        )

        if not selected_directory:

            return

        destination_result = (
            self.destination_manager
            .set_destination(
                selected_directory
            )
        )

        if not destination_result["success"]:

            error_message = (
                destination_result["errors"][0]
                if destination_result["errors"]
                else "Unable to save backup destination."
            )

            QMessageBox.critical(
                self,
                "Backup Destination",
                error_message,
            )

            return

        self.activity_card.add_log(
            "Backup destination changed."
        )

        self.activity_card.add_log(
            selected_directory
        )

        self.status.setText(
            "β— Destination Ready"
        )

        self.status.setStyleSheet(
            f"color:{Theme.Colors.SUCCESS}; font-size:11pt;"
        )

    # ---------------------------------------------------------
    # Open Destination
    # ---------------------------------------------------------

    def _open_destination(self):

        result = (
            self.destination_manager
            .get_destination()
        )

        if not result["success"]:

            error_message = (
                result["errors"][0]
                if result["errors"]
                else "Unable to read backup destination."
            )

            QMessageBox.critical(
                self,
                "Backup Destination",
                error_message,
            )

            return

        destination_path = (
            result["data"][
                "destination_path"
            ]
        )

        destination = Path(
            destination_path
        )

        if not destination.exists():

            QMessageBox.warning(
                self,
                "Backup Destination",
                (
                    "The configured backup destination "
                    "is currently unavailable.\n\n"
                    f"{destination_path}"
                ),
            )

            return

        if not destination.is_dir():

            QMessageBox.warning(
                self,
                "Backup Destination",
                (
                    "The configured backup destination "
                    "is not a directory.\n\n"
                    f"{destination_path}"
                ),
            )

            return

        try:

            os.startfile(
                str(destination)
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Open Folder",
                str(error),
            )

    # ---------------------------------------------------------
    # Live Activity
    # ---------------------------------------------------------

    def _log_info(
        self,
        message,
    ):

        self.activity_card.add_log(
            message
        )

    def _log_success(
        self,
        message,
    ):

        self.activity_card.add_log(
            message
        )

    def _log_error(
        self,
        message,
    ):

        self.activity_card.add_log(
            message
        )

    # ---------------------------------------------------------
    # Finished
    # ---------------------------------------------------------

    def _backup_finished(
        self,
        result,
    ):

        self.progress_card.reset()

        if not result.get(
            "success",
            False,
        ):

            self.status.setText(
                "β— Backup Failed"
            )

            self.status.setStyleSheet(
                "color:#dc2626; font-size:11pt;"
            )

            return

        data = (
            result.get(
                "data",
                {}
            )
            or {}
        )

        customer = (
            data.get(
                "customer",
                {}
            )
            or {}
        )

        statistics = (
            data.get(
                "statistics",
                {}
            )
            or {}
        )

        # -----------------------------------------------------
        # Customer Information
        # -----------------------------------------------------

        self.customer_card.set_customer(

            customer=customer.get(
                "customer",
                socket.gethostname(),
            ),

            sql_server=customer.get(
                "sql_server",
                (
                    database_context.active().get(
                        "server",
                        "-"
                    )
                    if database_context.active()
                    else "-"
                )
            ),

            database=customer.get(
                "database",
                (
                    database_context.active().get(
                        "name",
                        "-"
                    )
                    if database_context.active()
                    else "-"
                )
            ),

            database_version=customer.get(
                "database_version",
                "-"
            ),

            cloud=customer.get(
                "cloud",
                "Not configured"
            ),

            destination=customer.get(
                "destination",
                "-"
            ),

            last_backup=customer.get(
                "last_backup",
                "-"
            ),

            next_backup=customer.get(
                "next_backup",
                "-"
            ),

        )

        # -----------------------------------------------------
        # Backup Statistics
        # -----------------------------------------------------

        self.statistics_card.set_statistics(

            files=statistics.get(
                "files",
                0,
            ),

            size=statistics.get(
                "zip_size",
                "0 B",
            ),

            duration=statistics.get(
                "duration",
                "00:00",
            ),

            compression=statistics.get(
                "compression",
                "0 %",
            ),

        )

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        self.status.setText(
            "🟢 Έτοιμο"
        )

        self.status.setStyleSheet(
            f"color:{Theme.Colors.SUCCESS}; font-size:11pt;"
        )
