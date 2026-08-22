from __future__ import annotations

from pathlib import Path


class FileCollector:
    """
    Συλλέγει όλα τα αρχεία που πρέπει να μπουν στο backup.

    Δεν αντιγράφει αρχεία.
    Δεν κάνει συμπίεση.

    Απλώς επιστρέφει τη λίστα των αρχείων που βρέθηκαν.
    """

    def __init__(self) -> None:
        self.files: list[Path] = []

    # ---------------------------------------------------------

    def clear(self) -> None:
        """Καθαρίζει την τρέχουσα λίστα αρχείων."""

        self.files.clear()

    # ---------------------------------------------------------

    def add_file(self, file_path: str | Path) -> bool:
        """
        Προσθέτει ένα αρχείο εάν υπάρχει.
        """

        path = Path(file_path)

        if not path.exists():
            return False

        if not path.is_file():
            return False

        self.files.append(path)

        return True

    # ---------------------------------------------------------

    def add_directory(
        self,
        directory: str | Path,
        recursive: bool = True,
    ) -> int:
        """
        Συλλέγει όλα τα αρχεία ενός φακέλου.

        Επιστρέφει πόσα αρχεία βρέθηκαν.
        """

        path = Path(directory)

        if not path.exists():
            return 0

        if not path.is_dir():
            return 0

        iterator = path.rglob("*") if recursive else path.glob("*")

        count = 0

        for item in iterator:

            if item.is_file():
                self.files.append(item)
                count += 1

        return count

    # ---------------------------------------------------------

    def get_files(self) -> list[Path]:
        """
        Επιστρέφει αντίγραφο της λίστας.
        """

        return list(self.files)

    # ---------------------------------------------------------

    def total_files(self) -> int:
        return len(self.files)

    # ---------------------------------------------------------

    def total_size(self) -> int:
        """
        Συνολικό μέγεθος όλων των αρχείων (bytes).
        """

        total = 0

        for file in self.files:
            total += file.stat().st_size

        return total