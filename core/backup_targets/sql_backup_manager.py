from pathlib import Path
from datetime import datetime
import re

import pyodbc

from core.common.result import Result
from core.database.database_context import database_context
from core.database.udl_reader import UDLReader


class SQLBackupManager:

    SYSTEM_DATABASES = [
        "master",
        "model",
        "msdb",
        "tempdb",
    ]

    # ---------------------------------------------------------
    # UDL
    # ---------------------------------------------------------

    def _get_active_udl(self):

        udl_path = database_context.active_udl()

        if not udl_path:

            raise RuntimeError(
                "No database selected. Please select a database before starting the backup."
            )

        return Path(udl_path)

    def _get_database_connection(self):

        udl_path = self._get_active_udl()

        reader = UDLReader(
            str(udl_path)
        )

        connection_string = (
            reader.get_connection_string()
        )

        return reader, connection_string

    # ---------------------------------------------------------
    # SQL Directory
    # ---------------------------------------------------------

    def _create_sql_directory(
        self,
        destination_path,
    ):

        sql_directory = (
            Path(destination_path)
            / "SQL"
        )

        sql_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return sql_directory

    # ---------------------------------------------------------
    # SQL Connection
    # ---------------------------------------------------------

    def _connect(self):

        reader, connection_string = (
            self._get_database_connection()
        )

        connection = pyodbc.connect(
            connection_string,
            autocommit=True,
            timeout=30,
        )

        return (
            reader,
            connection,
        )

    # ---------------------------------------------------------
    # Database List
    # ---------------------------------------------------------

    def _get_user_databases(
        self,
        connection,
    ):

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sys.databases
            WHERE name NOT IN (?, ?, ?, ?)
            ORDER BY name
            """,
            self.SYSTEM_DATABASES[0],
            self.SYSTEM_DATABASES[1],
            self.SYSTEM_DATABASES[2],
            self.SYSTEM_DATABASES[3],
        )

        databases = []

        for row in cursor.fetchall():

            database_name = row[0]

            if database_name:

                databases.append(
                    str(database_name)
                )

        return databases

    # ---------------------------------------------------------
    # SQL Identifier
    # ---------------------------------------------------------

    @staticmethod
    def _quote_identifier(
        value,
    ):

        return (
            "["
            + str(value).replace(
                "]",
                "]]",
            )
            + "]"
        )

    # ---------------------------------------------------------
    # Backup Database
    # ---------------------------------------------------------

    def _backup_database(
        self,
        connection,
        database_name,
        sql_directory,
    ):

        timestamp = datetime.now().strftime(
            "%d%m%Y_%H%M%S"
        )

        backup_file_name = (
            f"{database_name}_{timestamp}.bak"
        )

        backup_file_path = (
            sql_directory
            / backup_file_name
        ).resolve()

        database_identifier = (
            self._quote_identifier(
                database_name
            )
        )

        backup_path_sql = (
            str(backup_file_path)
            .replace(
                "'",
                "''",
            )
        )

        command = (
            f"BACKUP DATABASE "
            f"{database_identifier} "
            f"TO DISK = N'{backup_path_sql}' "
            f"WITH INIT"
        )

        cursor = connection.cursor()

        try:

            cursor.execute(
                command
            )

            while cursor.nextset():
                pass

            success = (
                backup_file_path.exists()
                and backup_file_path.stat().st_size > 0
            )

            return {
                "success": success,
                "database_name": database_name,
                "backup_file": str(
                    backup_file_path
                ),
                "stdout": (
                    "Backup completed successfully."
                    if success
                    else "Backup file was not created."
                ),
                "stderr": "",
            }

        except Exception as error:

            return {
                "success": False,
                "database_name": database_name,
                "backup_file": str(
                    backup_file_path
                ),
                "stdout": "",
                "stderr": str(error),
            }

    # ---------------------------------------------------------
    # All Databases
    # ---------------------------------------------------------

    def _backup_all_databases(
        self,
        connection,
        user_databases,
        sql_directory,
    ):

        successful_backups = []
        failed_backups = []

        for database_name in user_databases:

            backup_result = (
                self._backup_database(
                    connection=connection,
                    database_name=database_name,
                    sql_directory=sql_directory,
                )
            )

            if backup_result["success"]:

                successful_backups.append(
                    backup_result
                )

            else:

                failed_backups.append(
                    backup_result
                )

        return (
            successful_backups,
            failed_backups,
        )

    # ---------------------------------------------------------
    # Information File
    # ---------------------------------------------------------

    def _generate_sql_information_file(
        self,
        sql_directory,
        udl_path,
        server_name,
        database_name,
        user_databases,
        successful_backups,
        failed_backups,
    ):

        information_file = (
            sql_directory
            / "SQL_Information.txt"
        )

        with open(
            information_file,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "SUNSOFT SQL BACKUP INFORMATION\n"
            )

            file.write(
                "=" * 50 + "\n\n"
            )

            file.write(
                f"UDL : {udl_path}\n"
            )

            file.write(
                f"SQL Server : {server_name}\n"
            )

            file.write(
                f"Selected Database : {database_name}\n\n"
            )

            file.write(
                "USER DATABASES\n"
            )

            file.write(
                "-" * 50 + "\n"
            )

            if not user_databases:

                file.write(
                    "NONE\n"
                )

            else:

                for database in user_databases:

                    file.write(
                        f"{database}\n"
                    )

            file.write(
                "\nSUCCESSFUL BACKUPS\n"
            )

            file.write(
                "-" * 50 + "\n"
            )

            if not successful_backups:

                file.write(
                    "NONE\n"
                )

            else:

                for backup in successful_backups:

                    file.write(
                        f"{Path(backup['backup_file']).name}\n"
                    )

            file.write(
                "\nFAILED BACKUPS\n"
            )

            file.write(
                "-" * 50 + "\n"
            )

            if not failed_backups:

                file.write(
                    "NONE\n"
                )

            else:

                for backup in failed_backups:

                    file.write(
                        f"{backup['database_name']} : "
                        f"{backup['stderr']}\n"
                    )

        return str(
            information_file
        )

    # ---------------------------------------------------------
    # Main Backup
    # ---------------------------------------------------------

    def backup(
        self,
        destination_path,
    ):

        connection = None

        try:

            udl_path = (
                self._get_active_udl()
            )

            reader = UDLReader(
                str(udl_path)
            )

            server_name = (
                reader.get_server_name()
            )

            selected_database = (
                reader.get_database_name()
            )

            if not selected_database:

                return Result.error(
                    "The selected UDL does not contain a database name."
                )

            sql_directory = (
                self._create_sql_directory(
                    destination_path
                )
            )

            connection = pyodbc.connect(
                reader.get_connection_string(),
                autocommit=True,
                timeout=30,
            )

            user_databases = (
                self._get_user_databases(
                    connection
                )
            )

            #
            # IMPORTANT:
            #
            # The UDL selects the SQL Server.
            # The UDL also selects the database.
            #
            # We backup the selected database first.
            #

            databases_to_backup = [
                selected_database
            ]

            #
            # If other user databases exist on
            # the same SQL Server, include them too.
            #

            for database_name in user_databases:

                if (
                    database_name
                    not in databases_to_backup
                ):

                    databases_to_backup.append(
                        database_name
                    )

            successful_backups, failed_backups = (
                self._backup_all_databases(
                    connection=connection,
                    user_databases=databases_to_backup,
                    sql_directory=sql_directory,
                )
            )

            sql_information_file = (
                self._generate_sql_information_file(
                    sql_directory=sql_directory,
                    udl_path=str(
                        udl_path
                    ),
                    server_name=server_name,
                    database_name=selected_database,
                    user_databases=databases_to_backup,
                    successful_backups=successful_backups,
                    failed_backups=failed_backups,
                )
            )

            generated_files = [
                Path(
                    backup["backup_file"]
                ).name
                for backup in successful_backups
            ]

            generated_files.append(
                Path(
                    sql_information_file
                ).name
            )

            if not successful_backups:

                return Result.error(
                    "No SQL databases were backed up."
                )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "udl_path": str(
                        udl_path
                    ),
                    "server_name": server_name,
                    "selected_database":
                        selected_database,
                    "sql_directory": str(
                        sql_directory
                    ),
                    "user_databases":
                        databases_to_backup,
                    "successful_backups":
                        successful_backups,
                    "failed_backups":
                        failed_backups,
                    "generated_files":
                        generated_files,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

        finally:

            if connection is not None:

                try:

                    connection.close()

                except Exception:

                    pass