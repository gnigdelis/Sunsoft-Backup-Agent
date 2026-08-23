from pathlib import Path

from PySide6.QtCore import QObject

from core.services.backup_service import backup_service
from core.database.database_context import database_context
from core.common.result import Result


class BackupController(QObject):
    """
    Connects the BackupService with the UI.

    Widgets communicate only with this controller and
    never directly with the BackupRunner.
    """

    def __init__(self, parent=None):

        super().__init__(parent)

        self.runner = backup_service.runner

    # -------------------------------------------------
    # Backup Commands
    # -------------------------------------------------

    def start_backup(self):

        # -------------------------------------------------
        # Database Selection Validation
        # -------------------------------------------------

        if not database_context.is_selected():

            return Result.error(
                "No database selected. "
                "Please select a database before starting the backup."
            )

        udl_path = (
            database_context.active_udl()
        )

        if not udl_path:

            return Result.error(
                "No database selected. "
                "Please select a database before starting the backup."
            )

        if not Path(udl_path).exists():

            return Result.error(
                "The selected UDL file is no longer available.\n"
                f"UDL: {udl_path}"
            )

        # -------------------------------------------------
        # Start Backup
        # -------------------------------------------------

        backup_service.start_backup()

        return Result.success(
            data={
                "udl_path": udl_path,
            }
        )

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    @property
    def is_running(self):

        return self.runner.thread is not None

    # -------------------------------------------------
    # Signals
    # -------------------------------------------------

    @property
    def progress_changed(self):

        return self.runner.progress_changed

    @property
    def log_info(self):

        return self.runner.log_info

    @property
    def log_success(self):

        return self.runner.log_success

    @property
    def log_error(self):

        return self.runner.log_error

    @property
    def finished(self):

        return self.runner.finished
