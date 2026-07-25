from core.backup_event_emitter import BackupEventEmitter


class ProgressTracker:

    def __init__(
        self,
        events: BackupEventEmitter,
        total_steps: int,
    ):

        self.events = events
        self.total_steps = total_steps
        self.current_step = 0

    @property
    def percentage(self) -> int:

        if self.total_steps == 0:
            return 0

        return int(
            (self.current_step / self.total_steps) * 100
        )

    def start(
        self,
        task: str,
    ):

        self.current_step = 0

        self.events.emit_progress(
            self.current_step,
            self.total_steps,
            task,
        )

    def next(
        self,
        task: str,
    ):

        if self.current_step < self.total_steps:
            self.current_step += 1

        self.events.emit_progress(
            self.current_step,
            self.total_steps,
            task,
        )

    def finish(self):

        self.current_step = self.total_steps

        self.events.emit_progress(
            self.current_step,
            self.total_steps,
            "Ολοκληρώθηκε",
        )

    def reset(self):

        self.current_step = 0

        self.events.emit_progress(
            0,
            self.total_steps,
            "Αναμονή...",
        )