from pathlib import Path
from datetime import datetime
import subprocess

from core.common.result import Result


class SQLBackupManager:

    SYSTEM_DATABASES = [
        "master",
        "model",
        "msdb",
        "tempdb",
    ]

    def _create_sql_directory(self, destination_path):

        sql_directory = (
            Path(destination_path)
            / "SQL"
        )

        sql_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return sql_directory

    def _get_user_databases(self):

        command = (
            'sqlcmd -S localhost -C '
            '-Q "SELECT name FROM sys.databases"'
        )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
        )

        databases = []

        for line in result.stdout.splitlines():

            database_name = line.strip()

            if not database_name:
                continue

            if database_name == "name":
                continue

            if "-----" in database_name:
                continue

            if "rows affected" in database_name:
                continue

            if database_name in self.SYSTEM_DATABASES:
                continue

            databases.append(database_name)

        return databases

    def _backup_database(
        self,
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

        command = (
            f"sqlcmd -S localhost -C "
            f"-Q \"BACKUP DATABASE [{database_name}] "
            f"TO DISK='{backup_file_path}' "
            f"WITH INIT\""
        )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
        )

        success = (
            "BACKUP DATABASE successfully processed"
            in result.stdout
        )

        return {
            "success": success,
            "database_name": database_name,
            "backup_file": str(backup_file_path),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def _backup_all_databases(
        self,
        user_databases,
        sql_directory,
    ):

        successful_backups = []
        failed_backups = []

        for database_name in user_databases:

            backup_result = self._backup_database(
                database_name=database_name,
                sql_directory=sql_directory,
            )

            if backup_result["success"]:
                successful_backups.append(
                    backup_result
                )
            else:
                failed_backups.append(
                    backup_result
                )

        return successful_backups, failed_backups

    def _generate_sql_information_file(
        self,
        sql_directory,
        user_databases,
        successful_backups,
        failed_backups,
    ):

        information_file = (
            sql_directory / "SQL_Information.txt"
        )

        with open(
            information_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("SUNSOFT SQL BACKUP INFORMATION\n")
            file.write("=" * 50 + "\n\n")

            file.write("USER DATABASES\n")
            file.write("-" * 50 + "\n")

            for database in user_databases:
                file.write(f"{database}\n")

            file.write("\nSUCCESSFUL BACKUPS\n")
            file.write("-" * 50 + "\n")

            for backup in successful_backups:
                file.write(
                    f"{Path(backup['backup_file']).name}\n"
                )

            file.write("\nFAILED BACKUPS\n")
            file.write("-" * 50 + "\n")

            if not failed_backups:
                file.write("NONE\n")
            else:
                for backup in failed_backups:
                    file.write(
                        f"{backup['database_name']}\n"
                    )

        return str(information_file)

    def backup(self, destination_path):

        try:

            sql_directory = self._create_sql_directory(
                destination_path
            )

            user_databases = (
                self._get_user_databases()
            )

            successful_backups, failed_backups = (
                self._backup_all_databases(
                    user_databases=user_databases,
                    sql_directory=sql_directory,
                )
            )

            sql_information_file = (
                self._generate_sql_information_file(
                    sql_directory=sql_directory,
                    user_databases=user_databases,
                    successful_backups=successful_backups,
                    failed_backups=failed_backups,
                )
            )

            generated_files = [
                Path(backup["backup_file"]).name
                for backup in successful_backups
            ]

            generated_files.append(
                Path(sql_information_file).name
            )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "sql_directory": str(sql_directory),
                    "user_databases": user_databases,
                    "successful_backups": successful_backups,
                    "failed_backups": failed_backups,
                    "generated_files": generated_files,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )