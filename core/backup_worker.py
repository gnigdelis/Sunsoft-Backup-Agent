from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from core.backup_pipeline import (
    BackupPipeline,
)

from core.backup_event_emitter import (
    BackupEventEmitter,
)


class BackupWorker(QObject):

    #
    # Live Logs
    #

    log_info = Signal(str)
    log_success = Signal(str)
    log_error = Signal(str)

    #
    # Progress
    #

    progress_changed = Signal(
        int,    # percentage
        int,    # current step
        int,    # total steps
        str,    # current task
    )

    #
    # Finished
    #

    finished = Signal(dict)

    def __init__(self):

        super().__init__()

        self.events = BackupEventEmitter()

        #
        # Forward Log Signals
        #

        self.events.log_info.connect(
            self.log_info.emit
        )

        self.events.log_success.connect(
            self.log_success.emit
        )

        self.events.log_error.connect(
            self.log_error.emit
        )

        #
        # Forward Progress Signals
        #

        self.events.progress_changed.connect(
            self.progress_changed.emit
        )

    @Slot()
    def run(self):

        pipeline = BackupPipeline(
            self.events
        )

        result = pipeline.execute()

        self.finished.emit(
            result
        )