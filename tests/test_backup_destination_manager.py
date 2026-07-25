from pprint import pprint

from core.destination.backup_destination_manager import (
    BackupDestinationManager,
)


manager = BackupDestinationManager()


print("\nDESTINATION VALIDATION\n")

pprint(
    manager.validate_destination()
)


print("\nCOPY BACKUP FILE\n")

pprint(
    manager.copy_backup_file(
        "backup_test.zip"
    )
)


print("\nSTORAGE HEALTH CHECK\n")

pprint(
    manager.get_storage_health()
)