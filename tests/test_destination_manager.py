from pprint import pprint

from core.destination_manager import (
    DestinationManager,
)


manager = DestinationManager()

result = manager.copy_backup(
    source_file=r"C:\Windows\notepad.exe",
    destination_path="backup_destination",
)

print(type(result))
print()

pprint(result)