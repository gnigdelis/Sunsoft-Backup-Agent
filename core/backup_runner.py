from threading import Event

from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
)

from core.backup_worker import BackupWorker


class BackupRunner(QObject):

    finished = Signal(dict)

    log_info = Signal(str)
    log_success = Signal(str)
    log_error = Signal(str)

    progress_changed = Signal(
        int,
        int,
        int,
        str,
    )

    def __init__(self):

        super().__init__()

        self.thread = None
        self.worker = None
        self.cancel_event = None

    def start(self):

        # Already running.
        if self.thread is not None:
            return

        self.cancel_event = Event()

        self.thread = QThread()

        self.worker = BackupWorker(
            self.cancel_event
        )

        self.worker.moveToThread(
            self.thread
        )

        # -------------------------------------------------
        # Worker
        # -------------------------------------------------

        self.thread.started.connect(
            self.worker.run
        )

        # -------------------------------------------------
        # Signals
        # -------------------------------------------------

        self.worker.log_info.connect(
            self.log_info
        )

        self.worker.log_success.connect(
            self.log_success
        )

        self.worker.log_error.connect(
            self.log_error
        )

        self.worker.progress_changed.connect(
            self.progress_changed
        )

        self.worker.finished.connect(
            self.finished
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        # -------------------------------------------------
        # Cleanup
        # -------------------------------------------------

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.finished.connect(
            self.cleanup
        )

        self.thread.start()

    def cancel(self):

        if self.thread is None:
            return False

        if self.cancel_event is None:
            return False

        if self.cancel_event.is_set():
            return False

        self.cancel_event.set()

        self.log_info.emit(
            "Stopping backup at the next safe checkpoint..."
        )

        return True

    def cleanup(self):

        self.worker = None
        self.thread = None
        self.cancel_event = None