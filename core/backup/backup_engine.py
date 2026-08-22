from __future__ import annotations

from enum import Enum, auto
from typing import Callable


class BackupState(Enum):
    IDLE = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()


class BackupEngine:
    """
    Main Backup Engine.

    Είναι υπεύθυνος μόνο για τον συντονισμό της διαδικασίας.
    Δεν κάνει ο ίδιος:
        - αντιγραφή αρχείων
        - backup database
        - συμπίεση
        - upload

    Αυτά θα τα αναλάβουν άλλα modules.
    """

    def __init__(self):

        self.state = BackupState.IDLE

        self.progress = 0

        self.current_step = ""

        self.on_progress: Callable[[int, str], None] | None = None

    # --------------------------------------------------

    def run(self):

        self.state = BackupState.RUNNING

        try:

            self._update(5, "Preparing backup...")

            self.validate()

            self._update(20, "Collecting files...")

            self.collect_files()

            self._update(45, "Backing up database...")

            self.backup_database()

            self._update(70, "Compressing backup...")

            self.compress()

            self._update(90, "Finalizing...")

            self.finish()

            self.state = BackupState.COMPLETED

            self._update(100, "Backup completed.")

        except Exception:

            self.state = BackupState.FAILED

            raise

    # --------------------------------------------------

    def validate(self):
        pass

    # --------------------------------------------------

    def collect_files(self):
        pass

    # --------------------------------------------------

    def backup_database(self):
        pass

    # --------------------------------------------------

    def compress(self):
        pass

    # --------------------------------------------------

    def finish(self):
        pass

    # --------------------------------------------------

    def _update(self, progress: int, message: str):

        self.progress = progress
        self.current_step = message

        if self.on_progress:
            self.on_progress(progress, message)