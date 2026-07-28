from PySide6.QtCore import QObject, QThread, Signal

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

    def start(self):

        #
        # ήδη τρέχει
        #

        if self.thread is not None:
            return

        self.thread = QThread()

        self.worker = BackupWorker()

        self.worker.moveToThread(
            self.thread
        )

        #
        # Signals
        #

        self.thread.started.connect(
            self.worker.run
        )

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

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.finished.connect(
            self.cleanup
        )

        self.thread.start()

    def cleanup(self):

        self.worker = None
        self.thread = None