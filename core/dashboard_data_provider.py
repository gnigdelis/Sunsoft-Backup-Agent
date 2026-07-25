from core.backup.backup_information import (
    BackupInformation,
)


class DashboardDataProvider:

    @staticmethod
    def get_last_backup():

        return BackupInformation.get_last_backup()

    @staticmethod
    def get_backup_files():

        return BackupInformation.get_backup_files()

    @staticmethod
    def get_database_count():

        return BackupInformation.get_database_count()

    @staticmethod
    def get_backup_size():

        return BackupInformation.get_backup_size()

    @staticmethod
    def get_backup_status():

        return BackupInformation.get_backup_status()