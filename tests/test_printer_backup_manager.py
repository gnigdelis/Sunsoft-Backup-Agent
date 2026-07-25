from pprint import pprint

from core.backup_targets.printer_backup_manager import (
    PrinterBackupManager,
)

manager = PrinterBackupManager()

result = manager.backup(
    destination_path="temp",
)

print(type(result))
print()

pprint(result)