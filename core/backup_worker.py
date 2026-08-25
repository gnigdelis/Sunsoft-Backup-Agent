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


class BackupCancelled(Exception):
    """Internal signal used to stop the active backup at a safe checkpoint."""


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

    def __init__(
        self,
        cancel_event=None,
    ):

        super().__init__()

        self.cancel_event = cancel_event

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

            file.write(
                text + "\n"
            )

    def _is_cancel_requested(self):

        return (
            self.cancel_event is not None
            and self.cancel_event.is_set()
        )

    def _cancelled_result(self):

        self.log_info.emit(
            "Backup cancellation requested."
        )

        return {
            "success": False,
            "cancelled": True,
            "errors": [
                "Backup cancelled by user."
            ],
            "data": {
                "status": "CANCELLED"
            },
        }

    def _install_cancellation_check(
        self,
        pipeline,
    ):

        original_info = pipeline.info
        original_progress = pipeline.progress
        original_error = pipeline.error

        def checked_info(message):

            if self._is_cancel_requested():
                raise BackupCancelled()

            original_info(message)

        def checked_progress(
            current_step,
            total_steps,
            task,
        ):

            if self._is_cancel_requested():
                raise BackupCancelled()

            original_progress(
                current_step,
                total_steps,
                task,
            )

        def checked_error(message):

            if self._is_cancel_requested():
                return

            original_error(message)

        pipeline.info = checked_info
        pipeline.progress = checked_progress
        pipeline.error = checked_error

    @Slot()
    def run(self):

        self.debug(
            "WORKER START"
        )

        try:

            if self._is_cancel_requested():

                self.finished.emit(
                    self._cancelled_result()
                )

                return

            self.debug(
                "Creating Pipeline"
            )

            pipeline = BackupPipeline(
                self.events
            )

            self._install_cancellation_check(
                pipeline
            )

            self.debug(
                "Executing Pipeline"
            )

            result = pipeline.execute()

            self.debug(
                "Pipeline Finished"
            )

            self.debug(
                str(result)
            )

            # A cancellation can arrive immediately after the
            # final pipeline checkpoint and before execute()
            # returns. Treat that run as cancelled as well.
            if self._is_cancel_requested():

                result = (
                    self._cancelled_result()
                )

            self.debug(
                "Emitting finished"
            )

            self.finished.emit(
                result
            )

            self.debug(
                "Finished emitted"
            )

        except BackupCancelled:

            self.debug(
                "Backup cancelled"
            )

            self.finished.emit(
                self._cancelled_result()
            )

        except Exception:

            self.debug(
                traceback.format_exc()
            )

            self.finished.emit(
                {
                    "success": False,
                    "cancelled": False,
                    "errors": [
                        traceback.format_exc()
                    ],
                }
            )

        self.debug(
            "WORKER END"
        )