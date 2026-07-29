from PySide6.QtCore import QObject

from core.services.backup_service import backup_service


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

        backup_service.start_backup()

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