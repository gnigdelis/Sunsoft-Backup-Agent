import json
from datetime import datetime, timedelta
from pathlib import Path

from PySide6.QtCore import QObject, QTimer, Signal

from core.controllers.backup_controller import BackupController


class BackupScheduler(QObject):

    schedule_changed = Signal()
    backup_triggered = Signal()
    error_occurred = Signal(str)

    SETTINGS_FILE = (
        Path.home()
        / "Sunsoft"
        / "SupportAgent"
        / "backup_schedule.json"
    )

    def __init__(self, parent=None):
        super().__init__(parent)

        self.controller = BackupController()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._run_scheduled_backup)

        self.enabled = False
        self.frequency_hours = 6
        self.start_time = "03:00"
        self.next_backup = None

        self._load()
        self._schedule_next()

    def _load(self):
        try:
            self.SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            if not self.SETTINGS_FILE.exists():
                return

            with self.SETTINGS_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.enabled = bool(data.get("enabled", False))
            self.frequency_hours = int(data.get("frequency_hours", 6))
            self.start_time = str(data.get("start_time", "03:00"))

            saved_next = data.get("next_backup")
            if saved_next:
                self.next_backup = datetime.fromisoformat(saved_next)

        except Exception as error:
            self.enabled = False
            self.next_backup = None
            self.error_occurred.emit(str(error))

    def _save(self):
        try:
            self.SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "enabled": self.enabled,
                "frequency_hours": self.frequency_hours,
                "start_time": self.start_time,
                "next_backup": self.next_backup.isoformat() if self.next_backup else None,
            }
            with self.SETTINGS_FILE.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except Exception as error:
            self.error_occurred.emit(str(error))

    def configure(self, enabled, frequency_hours, start_time):
        self.enabled = bool(enabled)
        self.frequency_hours = int(frequency_hours)
        self.start_time = str(start_time)
        self.timer.stop()

        if self.enabled:
            self.next_backup = self._calculate_next_backup()
        else:
            self.next_backup = None

        self._save()
        self._schedule_next()
        self.schedule_changed.emit()

    def _calculate_next_backup(self):
        now = datetime.now()
        try:
            hour, minute = map(int, self.start_time.split(":"))
        except Exception:
            hour, minute = 3, 0

        first_run = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0,
        )

        while first_run <= now:
            first_run += timedelta(hours=self.frequency_hours)

        return first_run

    def _schedule_next(self):
        self.timer.stop()
        if not self.enabled:
            return

        if not self.next_backup:
            self.next_backup = self._calculate_next_backup()
            self._save()

        delay = (self.next_backup - datetime.now()).total_seconds()
        self.timer.start(max(1000, int(delay * 1000)))

    def _run_scheduled_backup(self):
        if not self.enabled:
            return

        try:
            if getattr(self.controller, "is_running", False):
                self.next_backup = datetime.now() + timedelta(minutes=5)
                self._save()
                self._schedule_next()
                return

            self.controller.start_backup()
            self.backup_triggered.emit()

        except Exception as error:
            self.error_occurred.emit(str(error))

        self.next_backup = datetime.now() + timedelta(hours=self.frequency_hours)
        self._save()
        self._schedule_next()
        self.schedule_changed.emit()

    def is_enabled(self):
        return self.enabled

    def get_next_backup(self):
        return self.next_backup

    def get_frequency_hours(self):
        return self.frequency_hours

    def get_start_time(self):
        return self.start_time

    def stop(self):
        self.timer.stop()
