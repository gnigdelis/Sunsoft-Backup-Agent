from pprint import pprint

from core.backup_targets.common_files_sunsoft_manager import (
    CommonFilesSunsoftManager,
)

manager = CommonFilesSunsoftManager()

result = manager.backup(
    destination_path="temp",
)

print(type(result))
print()

pprint(result)