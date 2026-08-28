from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

import pyodbc

from core.database.database_context import database_context
from core.database.udl_reader import UDLReader


class RestoreEngine:

    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.cancel_requested = False

    def cancel(self):
        self.cancel_requested = True

    def _progress(self, percent, message):
        if self.progress_callback:
            self.progress_callback(int(percent), str(message))

    def _check_cancel(self):
        if self.cancel_requested:
            raise RuntimeError("Restore cancelled by user.")

    def inspect_backup(self, backup_file):

        backup_path = Path(backup_file)

        if not backup_path.exists():
            raise FileNotFoundError("Backup file does not exist.")

        if not backup_path.is_file():
            raise RuntimeError("Selected backup is not a file.")

        if backup_path.suffix.lower() != ".zip":
            raise RuntimeError("Selected backup is not a ZIP backup.")

        with zipfile.ZipFile(backup_path, "r") as archive:

            bad_file = archive.testzip()

            if bad_file:
                raise RuntimeError(
                    f"Backup is corrupted: {bad_file}"
                )

            names = archive.namelist()

        return {
            "backup_file": str(backup_path.resolve()),
            "backup_name": backup_path.name,
            "backup_size": backup_path.stat().st_size,
            "files": names,
            "sql": [
                name
                for name in names
                if name.lower().startswith("sql/")
                and name.lower().endswith(".bak")
            ],
            "registry": [
                name
                for name in names
                if name.lower().startswith("registry/")
                and name.lower().endswith(".reg")
            ],
            "printers": [
                name
                for name in names
                if name.lower().startswith("printers/")
            ],
            "form_path": [
                name
                for name in names
                if name.lower().startswith("form_path/")
            ],
            "programdata": [
                name
                for name in names
                if name.lower().startswith("programdata/")
            ],
            "configuration": [
                name
                for name in names
                if name.lower().startswith("configuration files/")
            ],
        }

    def _get_sql_connection_string(self):

        udl_path = database_context.active_udl()

        if not udl_path:
            raise RuntimeError("No database selected.")

        reader = UDLReader(udl_path)

        connection_string = reader.get_connection_string()

        connection_string = re.sub(
            r"DATABASE\s*=\s*[^;]*;?",
            "DATABASE=master;",
            connection_string,
            flags=re.IGNORECASE,
        )

        return connection_string

    def _connect_master(self):

        return pyodbc.connect(
            self._get_sql_connection_string(),
            autocommit=True,
            timeout=30,
        )

    def _get_default_paths(self, connection):

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                CAST(SERVERPROPERTY('InstanceDefaultDataPath') AS nvarchar(4000)),
                CAST(SERVERPROPERTY('InstanceDefaultLogPath') AS nvarchar(4000))
            """
        )

        row = cursor.fetchone()

        data_path = row[0] if row and row[0] else None
        log_path = row[1] if row and row[1] else None

        if not data_path:
            data_path = (
                os.environ.get(
                    "ProgramFiles",
                    r"C:\Program Files",
                )
                + r"\Microsoft SQL Server\MSSQL\Data"
            )

        if not log_path:
            log_path = data_path

        return Path(data_path), Path(log_path)

    def _quote_identifier(self, value):

        return "[" + str(value).replace("]", "]]") + "]"

    def _sql_literal(self, value):

        return "N'" + str(value).replace("'", "''") + "'"

    def _restore_database(
        self,
        connection,
        backup_file,
        database_name,
        index,
        total,
    ):

        self._check_cancel()

        self._progress(
            5 + int((index / max(total, 1)) * 35),
            f"Restoring database {database_name}...",
        )

        cursor = connection.cursor()

        backup_sql = self._sql_literal(backup_file)
        database_sql = self._quote_identifier(database_name)

        cursor.execute(
            f"""
            RESTORE FILELISTONLY
            FROM DISK = {backup_sql}
            """
        )

        rows = cursor.fetchall()

        data_path, log_path = self._get_default_paths(connection)

        moves = []

        data_index = 0
        log_index = 0

        for row in rows:

            logical_name = row[0]
            file_type = str(row[2]).upper()

            if file_type == "L":

                target_directory = log_path

                base_name = (
                    f"{database_name}_Log"
                    if log_index == 0
                    else f"{database_name}_Log_{log_index}"
                )

                target_file = (
                    target_directory / f"{base_name}.ldf"
                )

                log_index += 1

            else:

                target_directory = data_path

                base_name = (
                    database_name
                    if data_index == 0
                    else f"{database_name}_{data_index}"
                )

                extension = (
                    ".mdf"
                    if data_index == 0
                    else ".ndf"
                )

                target_file = (
                    target_directory
                    / f"{base_name}{extension}"
                )

                data_index += 1

            target_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            moves.append(
                "MOVE "
                + self._sql_literal(logical_name)
                + " TO "
                + self._sql_literal(target_file)
            )

        if not moves:
            raise RuntimeError(
                f"No database files found in {backup_file}."
            )

        restore_command = f"""
            RESTORE DATABASE {database_sql}
            FROM DISK = {backup_sql}
            WITH REPLACE,
            {", ".join(moves)},
            RECOVERY,
            STATS = 5
        """

        cursor.execute(restore_command)

        while cursor.nextset():
            self._check_cancel()

        self._progress(
            5 + int(((index + 1) / max(total, 1)) * 35),
            f"Database {database_name} restored.",
        )

    def _restore_sql(
        self,
        archive,
        sql_files,
        extraction_directory,
    ):

        if not sql_files:
            return 0

        archive.extractall(extraction_directory)

        connection = None

        try:

            connection = self._connect_master()

            total = len(sql_files)

            for index, archive_name in enumerate(sql_files):

                self._check_cancel()

                backup_file = (
                    extraction_directory / archive_name
                )

                database_name = Path(
                    archive_name
                ).stem

                match = re.match(
                    r"^(.*)_\d{8}_\d{6}$",
                    database_name,
                )

                if match:
                    database_name = match.group(1)

                self._restore_database(
                    connection,
                    str(backup_file.resolve()),
                    database_name,
                    index,
                    total,
                )

                connection.close()
                connection = self._connect_master()

            return total

        finally:

            if connection:
                connection.close()

    def _safe_extract_and_copy(
        self,
        archive,
        prefix,
        destination,
    ):

        members = [
            name
            for name in archive.namelist()
            if name.lower().startswith(prefix.lower())
        ]

        if not members:
            return 0

        destination = Path(destination)

        count = 0

        for member in members:

            self._check_cancel()

            if member.endswith("/"):
                continue

            relative = member[len(prefix):].lstrip("/\\")

            target = destination / relative

            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with archive.open(member, "r") as source:
                with open(target, "wb") as output:
                    shutil.copyfileobj(source, output)

            count += 1

        return count

    def _restore_files(self, archive):

        total = 0

        total += self._safe_extract_and_copy(
            archive,
            "form_path/",
            r"C:\form_path",
        )

        total += self._safe_extract_and_copy(
            archive,
            "ProgramData/Sunsoft/",
            r"C:\ProgramData\Sunsoft",
        )

        total += self._safe_extract_and_copy(
            archive,
            "Configuration Files/",
            r"C:\\",
        )

        return total

    def _restore_registry(self, archive):

        members = [
            name
            for name in archive.namelist()
            if name.lower().startswith("registry/")
            and name.lower().endswith(".reg")
        ]

        if not members:
            return 0

        temp_directory = Path(
            tempfile.mkdtemp(
                prefix="sunsoft_restore_registry_"
            )
        )

        try:

            count = 0

            for member in members:

                self._check_cancel()

                target = (
                    temp_directory
                    / Path(member).name
                )

                with archive.open(member, "r") as source:
                    with open(target, "wb") as output:
                        shutil.copyfileobj(source, output)

                result = subprocess.run(
                    [
                        "reg",
                        "import",
                        str(target),
                    ],
                    capture_output=True,
                    text=True,
                )

                if result.returncode != 0:
                    raise RuntimeError(
                        result.stderr
                        or f"Failed to import {member}."
                    )

                count += 1

            return count

        finally:

            shutil.rmtree(
                temp_directory,
                ignore_errors=True,
            )

    def _restore_printers(self, archive):

        members = [
            name
            for name in archive.namelist()
            if name.lower()
            == "printers/printerbackup.printerexport"
        ]

        if not members:
            return False

        temp_directory = Path(
            tempfile.mkdtemp(
                prefix="sunsoft_restore_printers_"
            )
        )

        try:

            export_file = (
                temp_directory
                / "PrinterBackup.printerExport"
            )

            with archive.open(members[0], "r") as source:
                with open(export_file, "wb") as output:
                    shutil.copyfileobj(source, output)

            printbrm = (
                r"C:\Windows\System32\spool\tools\PrintBrm.exe"
            )

            if not Path(printbrm).exists():
                raise RuntimeError(
                    "PrintBrm.exe was not found."
                )

            result = subprocess.run(
                [
                    printbrm,
                    "-R",
                    "-F",
                    str(export_file),
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    result.stderr
                    or "Printer restore failed."
                )

            return True

        finally:

            shutil.rmtree(
                temp_directory,
                ignore_errors=True,
            )

    def restore(
        self,
        backup_file,
        restore_database=True,
        restore_files=True,
        restore_registry=True,
        restore_printers=True,
    ):

        backup_info = self.inspect_backup(backup_file)

        self._progress(
            0,
            "Backup verified.",
        )

        self._check_cancel()

        extraction_directory = Path(
            tempfile.mkdtemp(
                prefix="sunsoft_restore_"
            )
        )

        try:

            with zipfile.ZipFile(
                backup_file,
                "r",
            ) as archive:

                results = {
                    "database": 0,
                    "files": 0,
                    "registry": 0,
                    "printers": False,
                    "backup": backup_info,
                }

                if restore_database:

                    self._progress(
                        5,
                        "Preparing database restore...",
                    )

                    results["database"] = self._restore_sql(
                        archive,
                        backup_info["sql"],
                        extraction_directory,
                    )

                self._check_cancel()

                if restore_files:

                    self._progress(
                        45,
                        "Restoring application files...",
                    )

                    results["files"] = self._restore_files(
                        archive
                    )

                self._check_cancel()

                if restore_registry:

                    self._progress(
                        70,
                        "Restoring registry settings...",
                    )

                    results["registry"] = self._restore_registry(
                        archive
                    )

                self._check_cancel()

                if restore_printers:

                    self._progress(
                        85,
                        "Restoring printers...",
                    )

                    results["printers"] = self._restore_printers(
                        archive
                    )

                self._progress(
                    100,
                    "Restore completed successfully.",
                )

                return results

        finally:

            shutil.rmtree(
                extraction_directory,
                ignore_errors=True,
            )

