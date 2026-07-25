from pprint import pprint

from core.backup_targets.registry_backup_manager import (
    RegistryBackupManager,
)


manager = RegistryBackupManager()

result = manager.backup(
    destination_path="temp",
)

print(type(result))
print()

pprint(result)