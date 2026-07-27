from pathlib import Path
import configparser

from core.common.result import Result


class SettingsManager:

    SETTINGS_FILE = "settings.ini"

    def create_default_settings(self):

        try:

            config = configparser.ConfigParser()

            config["BACKUP"] = {
                "automatic_backup": "False",
                "backup_time": "03:00",
            }

            config["DESTINATION"] = {
                "path": "",
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
                        self.SETTINGS_FILE,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def read_settings(self):

        try:

            config = configparser.ConfigParser()

            config.read(
                self.SETTINGS_FILE,
                encoding="utf-8",
            )

            return Result.success(
                data={
                    "status": "SUCCESS",

                    "automatic_backup":
                        config.getboolean(
                            "BACKUP",
                            "automatic_backup",
                        ),

                    "backup_time":
                        config.get(
                            "BACKUP",
                            "backup_time",
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
                        ),

                    "delete_temp_files":
                        config.getboolean(
                            "CLEANUP",
                            "delete_temp_files",
                        ),
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )