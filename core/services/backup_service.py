from core.backup_runner import BackupRunner


class BackupService:
    """
    Shared Backup Service.

    Holds a single BackupRunner instance that is shared
    across the entire application.
    """

    def __init__(self):
        self.runner = BackupRunner()

    def start_backup(self):
        if not self.runner.isRunning():
            self.runner.start()


backup_service = BackupService()