from pprint import pprint

from core.backup_targets.configuration_files_manager import (
    ConfigurationFilesManager,
)


manager = ConfigurationFilesManager()

result = manager.backup(
    destination_path="temp",
)

print(type(result))
print()

pprint(result)