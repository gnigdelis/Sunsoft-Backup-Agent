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

        self.progress_changed.emit(

            percentage,
            current_step,
            total_steps,
            task,

        )

        self.current_task.emit(
            task
        )