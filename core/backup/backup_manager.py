from __future__ import annotations

from core.backup.backup_engine import BackupEngine


class BackupManager:
    """
    Διαχειρίζεται την εκτέλεση των backup.

    Είναι το σημείο επικοινωνίας μεταξύ:
        • UI
        • Backup Engine
        • Workers (αργότερα)
    """

    def __init__(self):

        self.engine = BackupEngine()

        self.last_progress = 0
        self.last_message = ""

        self.engine.on_progress = self._on_progress

    # ---------------------------------------------------------

    def start_backup(self):

        self.engine.run()

    # ---------------------------------------------------------

    def _on_progress(
        self,
        progress: int,
        message: str,
    ):

        self.last_progress = progress
        self.last_message = message

        print(f"[{progress}%] {message}")