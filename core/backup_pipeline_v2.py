from core.common.result import Result


class BackupPipelineV2:

    def __init__(self, events=None):

        self.events = events

    # =========================================================
    # Events
    # =========================================================

    def info(self, message):

        if self.events:
            self.events.log_info.emit(message)

    def success(self, message):

        if self.events:
            self.events.log_success.emit(message)

    def warning(self, message):

        if self.events:
            self.events.log_warning.emit(message)

    def error(self, message):

        if self.events:
            self.events.log_error.emit(message)

    def progress(
        self,
        current_step,
        total_steps,
        task,
    ):

        if self.events:

            self.events.emit_progress(
                current_step=current_step,
                total_steps=total_steps,
                task=task,
            )

    # =========================================================
    # Pipeline
    # =========================================================

    def execute(self):

        try:

            self.info("Backup Pipeline v2")

            settings = self._load_settings()

            if not settings["success"]:
                return settings

            session = self._create_session()

            if not session["success"]:
                return session

            targets = self._run_targets(session)

            if not targets["success"]:
                return targets

            report = self._create_report(session)

            if not report["success"]:
                return report

            archive = self._create_zip(session)

            if not archive["success"]:
                return archive

            destination = self._copy_destination(
                archive,
                settings,
            )

            if not destination["success"]:
                return destination

            cleanup = self._cleanup(session)

            if not cleanup["success"]:
                return cleanup

            return Result.success()

        except Exception as error:

            return Result.error(str(error))

    # =========================================================
    # Steps
    # =========================================================

    def _load_settings(self):

        raise NotImplementedError()

    def _create_session(self):

        raise NotImplementedError()

    def _run_targets(self, session):

        raise NotImplementedError()

    def _create_report(self, session):

        raise NotImplementedError()

    def _create_zip(self, session):

        raise NotImplementedError()

    def _copy_destination(
        self,
        archive,
        settings,
    ):

        raise NotImplementedError()

    def _cleanup(self, session):

        raise NotImplementedError()