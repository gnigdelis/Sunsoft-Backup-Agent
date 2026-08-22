from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class BackupVerificationResult:
    """
    Αποτέλεσμα ελέγχου ενός backup.
    """

    is_valid: bool = True

    manifest_exists: bool = False

    zip_exists: bool = False

    manifest_valid: bool = False

    checksum_valid: bool = False

    size_valid: bool = False

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def add_warning(self, message: str) -> None:

        self.warnings.append(message)

    def add_error(self, message: str) -> None:

        self.errors.append(message)

        self.is_valid = False