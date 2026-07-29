from core.backup_runner import BackupRunner


class BackupService:
    """
    Shared Backup Service.

    Holds a single BackupRunner instance that is shared
    across the entire application.
    """

    def __init__(self):

        self.runner = BackupRunner()

    @property
    def is_running(self):

        return self.runner.thread is not None

    def start_backup(self):

        if self.is_running:
            return

        self.runner.start()


backup_service = BackupService()