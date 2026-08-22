from __future__ import annotations

import shutil
from pathlib import Path


class BackupValidator:
    """
    Εκτελεί όλους τους απαραίτητους ελέγχους
    πριν ξεκινήσει το backup.
    """

    def __init__(self) -> None:
        self.errors: list[str] = []

    # ---------------------------------------------------------

    def clear(self) -> None:
        self.errors.clear()

    # ---------------------------------------------------------

    def validate_file(self, file_path: str | Path) -> bool:

        path = Path(file_path)

        if not path.exists():
            self.errors.append(f"File not found: {path}")
            return False

        if not path.is_file():
            self.errors.append(f"Not a file: {path}")
            return False

        return True

    # ---------------------------------------------------------

    def validate_directory(self, directory: str | Path) -> bool:

        path = Path(directory)

        if not path.exists():
            self.errors.append(f"Directory not found: {path}")
            return False

        if not path.is_dir():
            self.errors.append(f"Not a directory: {path}")
            return False

        return True

    # ---------------------------------------------------------

    def validate_free_space(
        self,
        destination: str | Path,
        required_bytes: int,
    ) -> bool:

        usage = shutil.disk_usage(destination)

        if usage.free < required_bytes:

            self.errors.append(
                "Not enough free disk space."
            )

            return False

        return True

    # ---------------------------------------------------------

    def validate(self) -> bool:
        """
        Επιστρέφει True αν δεν υπάρχουν σφάλματα.
        """

        return len(self.errors) == 0