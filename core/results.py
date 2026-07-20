from dataclasses import dataclass


@dataclass
class BackupResult:

    success: bool
    message: str
    size: int = 0