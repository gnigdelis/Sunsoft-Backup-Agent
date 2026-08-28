from PySide6.QtCore import (
    QObject,
    Signal,
)


class RestoreWorker(QObject):

    started = Signal()

    progress = Signal(
        int,
        str,
    )

    finished = Signal(object)

    error = Signal(str)

    def __init__(
        self,
        service,
        backup_file,
        restore_database,
        restore_files,
        restore_registry,
        restore_printers,
    ):

        super().__init__()

        self.service = service

        self.backup_file = backup_file

        self.restore_database = restore_database

        self.restore_files = restore_files

        self.restore_registry = restore_registry

        self.restore_printers = restore_printers

    def run(self):

        try:

            self.started.emit()

            result = self.service.restore(
                backup_file=self.backup_file,
                restore_database=self.restore_database,
                restore_files=self.restore_files,
                restore_registry=self.restore_registry,
                restore_printers=self.restore_printers,
                progress_callback=self.report_progress,
            )

            self.finished.emit(
                result
            )

        except Exception as ex:

            self.error.emit(
                str(ex)
            )

    def report_progress(
        self,
        percent,
        message,
    ):

        self.progress.emit(
            int(percent),
            str(message),
        )


class RestoreController(QObject):

    started = Signal()

    progress = Signal(
        int,
        str,
    )

    finished = Signal(object)

    error = Signal(str)

    def __init__(
        self,
        service,
        thread,
        backup_file,
        restore_database=True,
        restore_files=True,
        restore_registry=True,
        restore_printers=True,
    ):

        super().__init__()

        self.service = service

        self.thread = thread

        self.worker = RestoreWorker(
            service,
            backup_file,
            restore_database,
            restore_files,
            restore_registry,
            restore_printers,
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.started.connect(
            self.started.emit
        )

        self.worker.progress.connect(
            self.progress.emit
        )

        self.worker.finished.connect(
            self.finished.emit
        )

        self.worker.error.connect(
            self.error.emit
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.error.connect(
            self.thread.quit
        )

        self.thread.finished.connect(
            self.worker.deleteLater
        )

    def start(self):

        self.thread.start()

    def stop(self):

        self.service.cancel()
