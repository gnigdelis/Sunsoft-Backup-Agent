from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

import traceback

from core.backup_pipeline import (
    BackupPipeline,
)

from core.backup_event_emitter import (
    BackupEventEmitter,
)


class BackupWorker(QObject):

    log_info = Signal(str)
    log_success = Signal(str)
    log_error = Signal(str)

    progress_changed = Signal(
        int,
        int,
        int,
        str,
    )

    finished = Signal(dict)

    def __init__(self):

        super().__init__()

        self.events = BackupEventEmitter()

        self.events.log_info.connect(
            self.log_info.emit
        )

        self.events.log_success.connect(
            self.log_success.emit
        )

        self.events.log_error.connect(
            self.log_error.emit
        )

        self.events.progress_changed.connect(
            self.progress_changed.emit
        )

    def debug(self, text):

        with open(
            "worker_debug.log",
            "a",
            encoding="utf-8",
        ) as file:

            file.write(text + "\n")

    @Slot()
    def run(self):

        self.debug("WORKER START")

        try:

            self.debug("Creating Pipeline")

            pipeline = BackupPipeline(
                self.events
            )

            self.debug("Executing Pipeline")

            result = pipeline.execute()

            self.debug("Pipeline Finished")

            self.debug(str(result))

            self.debug("Emitting finished")

            self.finished.emit(
                result
            )

            self.debug("Finished emitted")

        except Exception:

            self.debug(traceback.format_exc())

            self.finished.emit(
                {
                    "success": False,
                    "errors": [
                        traceback.format_exc()
                    ],
                }
            )

        self.debug("WORKER END")