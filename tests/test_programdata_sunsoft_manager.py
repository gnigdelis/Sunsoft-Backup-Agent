from pprint import pprint

from core.backup_targets.programdata_sunsoft_manager import (
    ProgramDataSunsoftManager,
)

manager = ProgramDataSunsoftManager()

result = manager.backup(
    destination_path="temp",
)

print(type(result))
print()
pprint(result)