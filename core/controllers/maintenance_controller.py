from PySide6.QtCore import (
    QObject,
    Signal,
)


class MaintenanceWorker(QObject):

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
        operation,
    ):

        super().__init__()

        self.service = service

        self.operation = operation

    def run(self):

        try:

            self.started.emit()

            if self.operation == "delete":

                result = (
                    self.service.delete_mydata(
                        progress_callback=self.report_progress
                    )
                )

            elif self.operation == "rebuild":

                result = (
                    self.service.rebuild(
                        progress_callback=self.report_progress
                    )
                )

            elif self.operation == "shrink":

                result = (
                    self.service.shrink(
                        progress_callback=self.report_progress
                    )
                )

            else:

                raise ValueError(
                    f"Unknown maintenance operation: "
                    f"{self.operation}"
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


class MaintenanceController(QObject):

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
        operation,
    ):

        super().__init__()

        self.service = service

        self.thread = thread

        self.worker = MaintenanceWorker(
            service,
            operation,
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.started.connect(
            self.on_started
        )

        self.worker.progress.connect(
            self.on_progress
        )

        self.worker.finished.connect(
            self.on_finished
        )

        self.worker.error.connect(
            self.on_error
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

        self.thread.finished.connect(
            self.on_thread_finished
        )

    def start(self):

        self.started.emit()

        self.thread.start()

    def stop(self):

        self.service.cancel()

    def on_started(self):

        self.started.emit()

    def on_progress(
        self,
        percent,
        message,
    ):

        self.progress.emit(
            percent,
            message,
        )

    def on_finished(
        self,
        result,
    ):

        self.finished.emit(
            result
        )

    def on_error(
        self,
        message,
    ):

        self.error.emit(
            message
        )

    def on_thread_finished(self):

        self.thread.deleteLater()