from core.restore.restore_engine import RestoreEngine


class RestoreService:

    def __init__(self):
        self.engine = None

    def inspect(
        self,
        backup_file,
    ):

        engine = RestoreEngine()

        return engine.inspect_backup(
            backup_file
        )

    def restore(
        self,
        backup_file,
        restore_database=True,
        restore_files=True,
        restore_registry=True,
        restore_printers=True,
        progress_callback=None,
    ):

        self.engine = RestoreEngine(
            progress_callback=progress_callback
        )

        try:

            return self.engine.restore(
                backup_file=backup_file,
                restore_database=restore_database,
                restore_files=restore_files,
                restore_registry=restore_registry,
                restore_printers=restore_printers,
            )

        finally:

            self.engine = None

    def cancel(self):

        if self.engine:

            self.engine.cancel()


restore_service = RestoreService()
