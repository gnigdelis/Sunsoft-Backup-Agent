import time

from PySide6.QtCore import (
    QObject,
    Signal,
)


class BackupEventEmitter(QObject):

    #
    # Live Logs
    #

    log_info = Signal(str)

    log_success = Signal(str)

    log_warning = Signal(str)

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
    # Current Task
    #

    current_task = Signal(str)

    #
    # UI update throttling
    #

    PROGRESS_UPDATE_INTERVAL = 0.075

    def __init__(self):

        super().__init__()

        self._last_progress_emit = 0.0
        self._last_percentage = None
        self._last_task = None

    def emit_progress(
        self,
        current_step: int,
        total_steps: int,
        task: str,
    ):

        if total_steps <= 0:

            percentage = 0

        else:

            percentage = int(
                (current_step / total_steps) * 100
            )

        now = time.monotonic()

        elapsed = (
            now - self._last_progress_emit
        )

        #
        # Always allow:
        # - first update
        # - percentage changes
        # - task changes
        # - 0%
        # - 100%
        #

        force_emit = (
            self._last_progress_emit == 0.0
            or percentage != self._last_percentage
            or task != self._last_task
            or percentage == 0
            or percentage >= 100
        )

        #
        # During a busy phase, limit UI updates.
        #

        if (
            not force_emit
            and elapsed < self.PROGRESS_UPDATE_INTERVAL
        ):

            return

        self._last_progress_emit = now
        self._last_percentage = percentage
        self._last_task = task

        self.progress_changed.emit(
            percentage,
            current_step,
            total_steps,
            task,
        )

        self.current_task.emit(
            task
        )