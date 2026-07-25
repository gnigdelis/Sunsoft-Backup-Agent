from pprint import pprint

from core.policy.backup_policy_manager import (
    BackupPolicyManager,
)


manager = BackupPolicyManager()


print("\nPOLICY CONFIGURATION\n")

pprint(
    manager.validate_configuration()
)


print("\nRUNTIME INFORMATION\n")

pprint(
    manager.get_runtime_information()
)


print("\nSHOULD TAKE BACKUP\n")

pprint(
    manager.should_take_backup()
)


print("\nUPDATE RUNTIME INFORMATION\n")

pprint(
    manager.update_runtime_information(
        backup_status="SUCCESS",
        duration_seconds=42,
    )
)


print("\nUPDATED RUNTIME INFORMATION\n")

pprint(
    manager.get_runtime_information()
)