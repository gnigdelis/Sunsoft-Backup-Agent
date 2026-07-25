from pprint import pprint

from core.backup_targets.sql_backup_manager import (
    SQLBackupManager,
)


manager = SQLBackupManager()

result = manager.backup(
    destination_path="temp",
)

print(type(result))
print()

pprint(result)