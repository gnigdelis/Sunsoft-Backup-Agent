from core.settings_manager import SettingsManager
from core.backup_session_manager import BackupSessionManager

from core.backup_targets.sql_backup_manager import SQLBackupManager
from core.backup_targets.registry_backup_manager import RegistryBackupManager
from core.backup_targets.configuration_files_manager import ConfigurationFilesManager
from core.backup_targets.programdata_sunsoft_manager import ProgramDataSunsoftManager
from core.backup_targets.form_path_manager import FormPathManager
from core.backup_targets.printer_backup_manager import PrinterBackupManager

from core.backup_report_manager import BackupReportManager
from core.zip_compression_manager import ZipCompressionManager
from core.destination_manager import DestinationManager
from core.cleanup_manager import CleanupManager

from core.common.result import Result


class BackupPipeline:

    def __init__(self, events=None):

        self.events = events

    # ---------------------------------------------------------
    # Events
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Pipeline
    # ---------------------------------------------------------

    def execute(self):

        try:

            total_steps = 11
            current_step = 0

            self.progress(current_step, total_steps, "Initialization")

            #
            # Settings
            #

            self.info("Ανάγνωση ρυθμίσεων...")

            settings_manager = SettingsManager()

            settings_result = settings_manager.read_settings()

            if not settings_result["success"]:

                self.error("Αποτυχία ανάγνωσης ρυθμίσεων.")
                return settings_result

            self.success("Οι ρυθμίσεις φορτώθηκαν.")

            destination_path = settings_result["data"]["destination_path"]
            delete_temp_files = settings_result["data"]["delete_temp_files"]

            current_step += 1
            self.progress(current_step, total_steps, "Settings")

            #
            # Session
            #

            self.info("Δημιουργία προσωρινού φακέλου...")

            session_manager = BackupSessionManager()

            session_result = session_manager.create_session("temp")

            if not session_result["success"]:

                self.error("Αποτυχία δημιουργίας προσωρινού φακέλου.")
                return session_result

            self.success("Ο προσωρινός φάκελος δημιουργήθηκε.")

            session_path = session_result["data"]["session_path"]
            session_name = session_result["data"]["session_name"]

            current_step += 1
            self.progress(current_step, total_steps, "Temporary Folder")

            #
            # Managers
            #

            managers = [

                ("SQL", SQLBackupManager()),
                ("Registry", RegistryBackupManager()),
                ("Configuration Files", ConfigurationFilesManager()),
                ("ProgramData", ProgramDataSunsoftManager()),
                ("Form Path", FormPathManager()),
                ("Printers", PrinterBackupManager()),

            ]

            report_lines = []

            for manager_name, manager in managers:

                self.info(f"Backup {manager_name}...")

                result = manager.backup(session_path)

                if result["success"]:

                    report_lines.append(
                        f"{manager_name} ........ SUCCESS"
                    )

                    self.success(
                        f"{manager_name} ολοκληρώθηκε."
                    )

                else:

                    report_lines.append(
                        f"{manager_name} ........ ERROR"
                    )

                    self.error(
                        f"{manager_name} απέτυχε."
                    )

                current_step += 1

                self.progress(
                    current_step,
                    total_steps,
                    manager_name,
                )

            #
            # Report
            #

            self.info("Δημιουργία Backup Report...")

            BackupReportManager().create_report(
                session_path=session_path,
                report_lines=report_lines,
            )

            self.success("Το Backup Report δημιουργήθηκε.")

            current_step += 1
            self.progress(current_step, total_steps, "Backup Report")

            #
            # ZIP
            #

            self.info("Δημιουργία ZIP...")

            zip_manager = ZipCompressionManager()

            zip_result = zip_manager.create_zip(
                source_directory=session_path,
                output_directory="temp",
            )

            if not zip_result["success"]:

                self.error("Αποτυχία δημιουργίας ZIP.")
                return zip_result

            self.success("Το ZIP δημιουργήθηκε.")

            zip_file = zip_result["data"]["zip_file"]

            current_step += 1
            self.progress(current_step, total_steps, "ZIP")

            #
            # Destination
            #

            if destination_path:

                self.info("Αντιγραφή στον προορισμό...")

                destination_result = DestinationManager().copy_backup(
                    source_file=zip_file,
                    destination_path=destination_path,
                )

                if not destination_result["success"]:

                    self.error("Αποτυχία αντιγραφής.")
                    return destination_result

                self.success("Η αντιγραφή ολοκληρώθηκε.")

            current_step += 1
            self.progress(current_step, total_steps, "Destination")

            #
            # Cleanup
            #

            if delete_temp_files:

                self.info("Καθαρισμός προσωρινών αρχείων...")

                CleanupManager().delete_directory(
                    session_path
                )

                self.success("Ο καθαρισμός ολοκληρώθηκε.")

            current_step += 1
            self.progress(current_step, total_steps, "Cleanup")

            return Result.success(

                data={

                    "status": "SUCCESS",
                    "session_name": session_name,
                    "session_path": session_path,
                    "zip_file": zip_file,

                }

            )

        except Exception as error:

            self.error(str(error))

            return Result.error(str(error))