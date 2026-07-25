from pprint import pprint

from core.backup.settings_backup_manager import (
    SettingsBackupManager,
)


manager = SettingsBackupManager()


result = manager.backup_settings()


pprint(result)