from pathlib import Path
import configparser
import os

from core.common.result import Result


class SettingsManager:

    SETTINGS_DIRECTORY = (
        Path(
            os.environ.get(
                "LOCALAPPDATA",
                Path.home(),
            )
        )
        / "Sunsoft Backup Agent"
    )

    SETTINGS_FILE = (
        SETTINGS_DIRECTORY
        / "settings.ini"
    )

    DEFAULT_BACKUP_FOLDER = (
        Path.home()
        / "SunsoftSupportAgent"
        / "Backups"
    )

    def create_default_settings(self):

        try:

            self.SETTINGS_DIRECTORY.mkdir(
                parents=True,
                exist_ok=True,
            )

            config = configparser.ConfigParser()

            config["BACKUP"] = {
                "automatic_backup": "False",
                "backup_time": "03:00",
            }

            config["DESTINATION"] = {
                "path": str(
                    self.DEFAULT_BACKUP_FOLDER
                ),
            }

            config["RETENTION"] = {
                "keep_last": "30",
            }

            config["CLEANUP"] = {
                "delete_temp_files": "True",
            }

            with open(
                self.SETTINGS_FILE,
                "w",
                encoding="utf-8",
            ) as settings_file:

                config.write(
                    settings_file
                )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "settings_file":
                        str(self.SETTINGS_FILE),
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def read_settings(self):

        try:

            if not self.SETTINGS_FILE.exists():

                result = (
                    self.create_default_settings()
                )

                if not result["success"]:

                    return result

            config = configparser.ConfigParser()

            config.read(
                self.SETTINGS_FILE,
                encoding="utf-8",
            )

            if not config.has_section(
                "DESTINATION"
            ):

                config["DESTINATION"] = {
                    "path": str(
                        self.DEFAULT_BACKUP_FOLDER
                    )
                }

            if not config.get(
                "DESTINATION",
                "path",
                fallback="",
            ).strip():

                config["DESTINATION"]["path"] = str(
                    self.DEFAULT_BACKUP_FOLDER
                )

                self._write_config(
                    config
                )

            return Result.success(
                data={
                    "status": "SUCCESS",

                    "automatic_backup":
                        config.getboolean(
                            "BACKUP",
                            "automatic_backup",
                            fallback=False,
                        ),

                    "backup_time":
                        config.get(
                            "BACKUP",
                            "backup_time",
                            fallback="03:00",
                        ),

                    "destination_path":
                        config.get(
                            "DESTINATION",
                            "path",
                        ),

                    "keep_last":
                        config.getint(
                            "RETENTION",
                            "keep_last",
                            fallback=30,
                        ),

                    "delete_temp_files":
                        config.getboolean(
                            "CLEANUP",
                            "delete_temp_files",
                            fallback=True,
                        ),
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def set_destination_path(
        self,
        destination_path,
    ):

        try:

            path = str(
                destination_path
            ).strip()

            if not path:

                return Result.error(
                    "Backup destination cannot be empty."
                )

            if not self.SETTINGS_FILE.exists():

                result = (
                    self.create_default_settings()
                )

                if not result["success"]:

                    return result

            config = configparser.ConfigParser()

            config.read(
                self.SETTINGS_FILE,
                encoding="utf-8",
            )

            if not config.has_section(
                "DESTINATION"
            ):

                config["DESTINATION"] = {}

            config["DESTINATION"]["path"] = path

            self._write_config(
                config
            )

            return Result.success(
                data={
                    "destination_path": path,
                    "settings_file":
                        str(self.SETTINGS_FILE),
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def reset_destination_path(self):

        return self.set_destination_path(
            str(self.DEFAULT_BACKUP_FOLDER)
        )

    def _write_config(
        self,
        config,
    ):

        self.SETTINGS_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.SETTINGS_FILE,
            "w",
            encoding="utf-8",
        ) as settings_file:

            config.write(
                settings_file
            )