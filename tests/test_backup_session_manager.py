from pprint import pprint

from core.backup_session_manager import (
    BackupSessionManager,
)


manager = BackupSessionManager()

result = manager.create_session(
    destination_path="temp",
)

print(type(result))
print()

pprint(result)