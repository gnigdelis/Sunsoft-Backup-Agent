from pathlib import Path
from datetime import datetime
import platform
import time

from core.settings_manager import SettingsManager
from core.backup_session_manager import BackupSessionManager

from core.database.database_context import database_context

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
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _get_session_statistics(
        session_path,
    ):

        session_directory = Path(
            session_path
        )

        file_count = 0
        total_size = 0

        if not session_directory.exists():

            return {
                "files": 0,
                "size_bytes": 0,
            }

        for file_path in session_directory.rglob("*"):

            if not file_path.is_file():

                continue

            try:

                file_count += 1

                total_size += (
                    file_path.stat().st_size
                )

            except OSError:

                continue

        return {
            "files": file_count,
            "size_bytes": total_size,
        }

    @staticmethod
    def _format_size(
        size_bytes,
    ):

        size = float(
            size_bytes
        )

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
        ]

        for unit in units:

            if size < 1024:

                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} PB"

    @staticmethod
    def _format_duration(
        seconds,
    ):

        total_seconds = max(
            0,
            int(round(seconds))
        )

        hours = total_seconds // 3600

        minutes = (
            total_seconds % 3600
        ) // 60

        remaining_seconds = (
            total_seconds % 60
        )

        if hours > 0:

            return (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{remaining_seconds:02d}"
            )

        return (
            f"{minutes:02d}:"
            f"{remaining_seconds:02d}"
        )

    # ---------------------------------------------------------
    # Database Validation
    # ---------------------------------------------------------

    def _validate_database_selection(self):

        if not database_context.is_selected():

            return Result.error(
                "No database selected. "
                "Please select a database before starting the backup."
            )

        udl_path = (
            database_context.active_udl()
        )

        if not udl_path:

            return Result.error(
                "No database selected. "
                "Please select a database before starting the backup."
            )

        udl_file = Path(
            udl_path
        )

        if not udl_file.exists():

            return Result.error(
                "The selected UDL file is no longer available.\n"
                f"UDL: {udl_path}"
            )

        if not udl_file.is_file():

            return Result.error(
                "The selected UDL path is not a file.\n"
                f"UDL: {udl_path}"
            )

        return Result.success(
            data={
                "udl_path": str(
                    udl_file
                ),
                "database": (
                    database_context.active()
                ),
            }
        )

    # ---------------------------------------------------------
    # Pipeline
    # ---------------------------------------------------------

    def execute(self):

        start_time = time.perf_counter()

        try:

            # -------------------------------------------------
            # Database Selection
            # -------------------------------------------------

            database_result = (
                self._validate_database_selection()
            )

            if not database_result["success"]:

                self.error(
                    database_result["errors"][0]
                )

                return database_result

            selected_database = (
                database_result["data"][
                    "database"
                ]
            )

            selected_udl = (
                database_result["data"][
                    "udl_path"
                ]
            )

            self.info(
                "Database selected: "
                + (
                    selected_database.get(
                        "name"
                    )
                    or "-"
                )
            )

            self.info(
                "UDL: "
                + selected_udl
            )

            # -------------------------------------------------
            # Initialization
            # -------------------------------------------------

            total_steps = 11
            current_step = 0

            self.progress(
                current_step,
                total_steps,
                "Initialization",
            )

            # -------------------------------------------------
            # Settings
            # -------------------------------------------------

            self.info(
                "Ανάγνωση ρυθμίσεων..."
            )

            settings_manager = (
                SettingsManager()
            )

            settings_result = (
                settings_manager.read_settings()
            )

            if not settings_result["success"]:

                self.error(
                    "Αποτυχία ανάγνωσης ρυθμίσεων."
                )

                return settings_result

            self.success(
                "Οι ρυθμίσεις φορτώθηκαν."
            )

            destination_path = (
                settings_result["data"][
                    "destination_path"
                ]
            )

            delete_temp_files = (
                settings_result["data"][
                    "delete_temp_files"
                ]
            )

            current_step += 1

            self.progress(
                current_step,
                total_steps,
                "Settings",
            )

            # -------------------------------------------------
            # Destination Validation
            # -------------------------------------------------

            self.info(
                "Έλεγχος προορισμού backup..."
            )

            destination_manager = (
                DestinationManager()
            )

            destination_result = (
                destination_manager
                .validate_destination(
                    destination_path
                )
            )

            if not destination_result["success"]:

                self.error(
                    "Ο προορισμός backup δεν είναι διαθέσιμος."
                )

                return destination_result

            self.success(
                "Ο προορισμός backup είναι διαθέσιμος."
            )

            current_step += 1

            self.progress(
                current_step,
                total_steps,
                "Destination Validation",
            )

            # -------------------------------------------------
            # Session
            # -------------------------------------------------

            self.info(
                "Δημιουργία προσωρινού φακέλου..."
            )

            session_manager = (
                BackupSessionManager()
            )

            session_result = (
                session_manager.create_session(
                    "temp"
                )
            )

            if not session_result["success"]:

                self.error(
                    "Αποτυχία δημιουργίας προσωρινού φακέλου."
                )

                return session_result

            self.success(
                "Προσωρινός φάκελος δημιουργήθηκε."
            )

            session_path = (
                session_result["data"][
                    "session_path"
                ]
            )

            session_name = (
                session_result["data"][
                    "session_name"
                ]
            )

            current_step += 1

            self.progress(
                current_step,
                total_steps,
                "Temporary Folder",
            )

            # -------------------------------------------------
            # Managers
            # -------------------------------------------------

            managers = [

                (
                    "SQL",
                    SQLBackupManager()
                ),

                (
                    "Registry",
                    RegistryBackupManager()
                ),

                (
                    "Configuration Files",
                    ConfigurationFilesManager()
                ),

                (
                    "ProgramData",
                    ProgramDataSunsoftManager()
                ),

                (
                    "Form Path",
                    FormPathManager()
                ),

                (
                    "Printers",
                    PrinterBackupManager()
                ),

            ]

            report_lines = []

            for manager_name, manager in managers:

                self.info(
                    f"Backup {manager_name}..."
                )

                result = manager.backup(
                    session_path
                )

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

            # -------------------------------------------------
            # Statistics Before ZIP
            # -------------------------------------------------

            session_statistics = (
                self._get_session_statistics(
                    session_path
                )
            )

            source_size_bytes = (
                session_statistics[
                    "size_bytes"
                ]
            )

            source_file_count = (
                session_statistics[
                    "files"
                ]
            )

            # -------------------------------------------------
            # Report
            # -------------------------------------------------

            self.info(
                "Δημιουργία Backup Report..."
            )

            report_result = (
                BackupReportManager()
                .create_report(
                    session_path=session_path,
                    report_lines=report_lines,
                )
            )

            if not report_result["success"]:

                self.error(
                    "Αποτυχία δημιουργίας Backup Report."
                )

                return report_result

            self.success(
                "Το Backup Report δημιουργήθηκε."
            )

            current_step += 1

            self.progress(
                current_step,
                total_steps,
                "Backup Report",
            )

            # -------------------------------------------------
            # ZIP
            # -------------------------------------------------

            self.info(
                "Δημιουργία ZIP..."
            )

            zip_manager = (
                ZipCompressionManager()
            )

            zip_result = (
                zip_manager.create_zip(
                    source_directory=session_path,
                    output_directory="temp",
                )
            )

            if not zip_result["success"]:

                self.error(
                    "Αποτυχία δημιουργίας ZIP."
                )

                return zip_result

            self.success(
                "Το ZIP δημιουργήθηκε."
            )

            zip_file = (
                zip_result["data"][
                    "zip_file"
                ]
            )

            zip_size_bytes = (
                zip_result["data"].get(
                    "zip_size",
                    0,
                )
            )

            current_step += 1

            self.progress(
                current_step,
                total_steps,
                "ZIP",
            )

            # -------------------------------------------------
            # Compression Statistics
            # -------------------------------------------------

            if source_size_bytes > 0:

                compression_percentage = (
                    (
                        1
                        - (
                            zip_size_bytes
                            / source_size_bytes
                        )
                    )
                    * 100
                )

                compression_percentage = max(
                    0,
                    min(
                        100,
                        compression_percentage,
                    ),
                )

            else:

                compression_percentage = 0

            # -------------------------------------------------
            # Destination
            # -------------------------------------------------

            self.info(
                "Αντιγραφή στον προορισμό..."
            )

            destination_result = (
                destination_manager
                .copy_backup(
                    source_file=zip_file,
                    destination_path=destination_path,
                )
            )

            if not destination_result["success"]:

                self.error(
                    "Αποτυχία αντιγραφής backup."
                )

                return destination_result

            self.success(
                "Η αντιγραφή ολοκληρώθηκε."
            )

            current_step += 1

            self.progress(
                current_step,
                total_steps,
                "Destination",
            )

            # -------------------------------------------------
            # Cleanup
            # -------------------------------------------------

            if delete_temp_files:

                self.info(
                    "Καθαρισμός προσωρινών αρχείων..."
                )

                CleanupManager().delete_directory(
                    session_path
                )

                self.success(
                    "Ο καθαρισμός ολοκληρώθηκε."
                )

            current_step += 1

            self.progress(
                current_step,
                total_steps,
                "Cleanup",
            )

            # -------------------------------------------------
            # Final Statistics
            # -------------------------------------------------

            elapsed_seconds = (
                time.perf_counter()
                - start_time
            )

            completed_at = (
                datetime.now().strftime(
                    "%H:%M:%S"
                )
            )

            backup_statistics = {

                "files":
                    source_file_count,

                "source_size_bytes":
                    source_size_bytes,

                "source_size":
                    self._format_size(
                        source_size_bytes
                    ),

                "zip_size_bytes":
                    zip_size_bytes,

                "zip_size":
                    self._format_size(
                        zip_size_bytes
                    ),

                "duration_seconds":
                    round(
                        elapsed_seconds,
                        2,
                    ),

                "duration":
                    self._format_duration(
                        elapsed_seconds
                    ),

                "compression":
                    f"{compression_percentage:.1f} %",

            }

            customer_information = {

                "customer":
                    platform.node(),

                "sql_server":
                    selected_database.get(
                        "server"
                    )
                    or "-",

                "destination":
                    str(destination_path),

                "cloud":
                    "Not configured",

                "last_backup":
                    completed_at,

            }

            # -------------------------------------------------
            # Finish
            # -------------------------------------------------

            return Result.success(

                data={

                    "status":
                        "SUCCESS",

                    "session_name":
                        session_name,

                    "session_path":
                        session_path,

                    "zip_file":
                        zip_file,

                    "destination_path":
                        str(destination_path),

                    "udl_path":
                        selected_udl,

                    "database":
                        selected_database,

                    "customer":
                        customer_information,

                    "statistics":
                        backup_statistics,

                }

            )

        except Exception as error:

            self.error(
                str(error)
            )

            return Result.error(
                str(error)
            )
