from dataclasses import dataclass


@dataclass(frozen=True)
class BackupStep:

    name: str


BACKUP_STEPS = [

    BackupStep(
        "Ρυθμίσεις"
    ),

    BackupStep(
        "Δημιουργία Session"
    ),

    BackupStep(
        "SQL Backup"
    ),

    BackupStep(
        "Registry Backup"
    ),

    BackupStep(
        "Configuration Files"
    ),

    BackupStep(
        "ProgramData"
    ),

    BackupStep(
        "Forms"
    ),

    BackupStep(
        "Printers"
    ),

    BackupStep(
        "Backup Report"
    ),

    BackupStep(
        "ZIP Compression"
    ),

    BackupStep(
        "Copy To Destination"
    ),

    BackupStep(
        "Cleanup"
    ),
]