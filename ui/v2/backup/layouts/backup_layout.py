from pathlib import Path
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
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

        self._update_connection_status(
            database_context.active()
        )

        if database_context.is_selected():
            self._update_customer_information()

        self._update_backup_controls()

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        self.setObjectName(
            "BackupLayout"
        )

        self.setStyleSheet(
            f"""
            QWidget#BackupLayout {{
                background: transparent;
                border: none;
            }}

            QWidget#BackupLayout QLabel {{
                background: transparent;
                border: none;
            }}
            """
        )

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            20,
            18,
            20,
            22
        )

        root.setSpacing(
            16
        )

        # ======================================================
        # HEADER
        # ======================================================

        header = QHBoxLayout()

        header.setContentsMargins(
            0,
            0,
            0,
            4
        )

        title_block = QVBoxLayout()

        title_block.setContentsMargins(
            0,
            0,
            0,
            0
        )

        title_block.setSpacing(
            2
        )

        title = QLabel(
            "Backup"
        )

        title.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                background:transparent;
                border:none;
                font-size:24pt;
                font-weight:700;
                padding:0;
            }}
            """
        )

        subtitle = QLabel(
            "Create, monitor and manage your system backups"
        )

        subtitle.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                background:transparent;
                border:none;
                font-size:10pt;
                padding:0;
            }}
            """
        )

        title_block.addWidget(
            title
        )

        title_block.addWidget(
            subtitle
        )

        header.addLayout(
            title_block
        )

        header.addStretch()

        # ======================================================
        # CONNECTION STATUS
        # ======================================================

        self.status = QLabel(
            "Not Connected"
        )

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.status.setMinimumWidth(
            120
        )

        self.status.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#ff9800;
                font-size:10pt;
                font-weight:700;
                padding:0 4px;
            }
            """
        )

        header.addWidget(
            self.status
        )

        root.addLayout(
            header
        )

        # ======================================================
        # TOOLBAR
        # ======================================================

        self.toolbar = BackupToolbar()

        root.addWidget(
            self.toolbar
        )

        # ======================================================
        # PROGRESS
        # ======================================================

        self.progress_card = ProgressCard()

        root.addWidget(
            self.progress_card
        )

        # ======================================================
        # LOWER AREA
        # ======================================================

        middle = QHBoxLayout()

        middle.setContentsMargins(
            0,
            4,
            0,
            4
        )

        middle.setSpacing(
            18
        )

        self.customer_card = CustomerCard()

        self.activity_card = LiveActivityCard()

        middle.addWidget(
            self.customer_card,
            1
        )

        middle.addWidget(
            self.activity_card,
            2
        )

        root.addLayout(
            middle,
            1
        )

        # ======================================================
        # STATISTICS
        # ======================================================

        self.statistics_card = StatisticsCard()

        root.addWidget(
            self.statistics_card
        )

    # ==========================================================
    # EVENTS
    # ==========================================================

    def connect_events(self):

        self.toolbar.start_backup.connect(
            self._start_backup
        )

        self.toolbar.cancel_backup.connect(
            self._cancel_backup
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

    # ==========================================================
    # DATABASE CHANGE
    # ==========================================================

    def _on_database_changed(
        self,
        database
    ):

        self._update_connection_status(
            database
        )

        if database:
            self._update_customer_information()
        else:
            self.customer_card.set_customer(
                customer="-",
                sql_server="-",
                destination="-",
                cloud="-",
                last_backup="-",
            )

    # ==========================================================
    # CONNECTION STATUS
    # ==========================================================

    def _update_connection_status(
        self,
        database
    ):

        if database:

            self.status.setText(
                "Connected"
            )

            self.status.setStyleSheet(
                """
                QLabel {
                    background:transparent;
                    border:none;
                    color:#53c653;
                    font-size:10pt;
                    font-weight:700;
                    padding:0 4px;
                }
                """
            )

        else:

            self.status.setText(
                "Not Connected"
            )

            self.status.setStyleSheet(
                """
                QLabel {
                    background:transparent;
                    border:none;
                    color:#ff9800;
                    font-size:10pt;
                    font-weight:700;
                    padding:0 4px;
                }
                """
            )

    # ==========================================================
    # BACKUP CONTROLS
    # ==========================================================

    def _update_backup_controls(self):

        self.toolbar.set_backup_running(
            self.backup_controller.is_running
        )

    # ==========================================================
    # CUSTOMER INFORMATION
    # ==========================================================

    def _update_customer_information(self):

        database = database_context.active()

        if not database:
            return

        destination = "-"

        result = (
            self.destination_manager.get_destination()
        )

        if result["success"]:

            destination = (
                result["data"].get(
                    "destination_path",
                    "-"
                )
            )

        self.customer_card.set_customer(
            customer=(
                database.get(
                    "name",
                    "-"
                )
                or "-"
            ),
            sql_server=(
                database.get(
                    "server",
                    "-"
                )
                or "-"
            ),
            destination=str(
                destination
            ),
            cloud="Not configured",
            last_backup="-",
        )

    # ==========================================================
    # START BACKUP
    # ==========================================================

    def _start_backup(self):

        if self.backup_controller.is_running:
            return

        self._update_backup_controls()

        self.activity_card.add_log(
            "Starting backup..."
        )

        result = (
            self.backup_controller.start_backup()
        )

        self._update_backup_controls()

        if result is not None:
            return

    # ==========================================================
    # CANCEL BACKUP
    # ==========================================================

    def _cancel_backup(self):

        if not self.backup_controller.is_running:
            return

        cancelled = (
            self.backup_controller.cancel_backup()
        )

        if cancelled:

            self.activity_card.add_log(
                "Backup cancellation requested. "
                "Waiting for the current safe checkpoint..."
            )

            self.toolbar.cancel_button.setEnabled(
                False
            )

    # ==========================================================
    # BROWSE DESTINATION
    # ==========================================================

    def _browse_destination(self):

        result = (
            self.destination_manager.get_destination()
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
            self.destination_manager.set_destination(
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

        self._update_customer_information()

        self.activity_card.add_log(
            "Backup destination changed."
        )

        self.activity_card.add_log(
            selected_directory
        )

    # ==========================================================
    # OPEN DESTINATION
    # ==========================================================

    def _open_destination(self):

        result = (
            self.destination_manager.get_destination()
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

    # ==========================================================
    # LOGGING
    # ==========================================================

    def _log_info(
        self,
        message
    ):

        self.activity_card.add_log(
            message
        )

    def _log_success(
        self,
        message
    ):

        self.activity_card.add_log(
            message
        )

    def _log_error(
        self,
        message
    ):

        self.activity_card.add_log(
            message
        )

    # ==========================================================
    # FINISHED
    # ==========================================================

    def _backup_finished(
        self,
        result
    ):

        self._update_backup_controls()

        self.progress_card.reset()

        if result.get(
            "cancelled",
            False
        ):

            self.activity_card.add_log(
                "Backup cancelled by user."
            )

            self.status.setText(
                "Not Connected"
                if not database_context.active()
                else "Connected"
            )

            return

        if not result.get(
            "success",
            False
        ):
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

        self.customer_card.set_customer(
            customer=customer.get(
                "customer",
                "-"
            ),
            sql_server=customer.get(
                "sql_server",
                "-"
            ),
            destination=customer.get(
                "destination",
                "-"
            ),
            cloud=customer.get(
                "cloud",
                "Not configured"
            ),
            last_backup=customer.get(
                "last_backup",
                "-"
            ),
        )

        self.statistics_card.set_statistics(
            files=statistics.get(
                "files",
                0
            ),
            size=statistics.get(
                "zip_size",
                "0 B"
            ),
            duration=statistics.get(
                "duration",
                "00:00"
            ),
            compression=statistics.get(
                "compression",
                "0 %"
            ),
        )

        self._update_connection_status(
            database_context.active()
        )