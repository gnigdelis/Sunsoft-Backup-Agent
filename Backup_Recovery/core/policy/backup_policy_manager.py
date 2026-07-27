import json
from datetime import datetime

from core.common.result import Result


class BackupPolicyManager:

    VALID_BACKUP_INTERVALS = [
        2,
        4,
        6,
        12,
        24,
    ]

    def load_configuration(self):

        with open(
            "settings/policy/backup_policy.json",
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def load_runtime(self):

        with open(
            "runtime/backup_runtime.json",
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def validate_configuration(self):

        try:

            configuration = (
                self.load_configuration()
            )

            interval = configuration[
                "backup_interval_hours"
            ]

            configuration_valid = (
                interval
                in self.VALID_BACKUP_INTERVALS
            )

            return Result.success(

                data={

                    "backup_interval_hours":
                        interval,

                    "configuration_valid":
                        configuration_valid,

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def get_runtime_information(self):

        try:

            runtime = self.load_runtime()

            return Result.success(
                data=runtime
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def should_take_backup(self):

        try:

            configuration = (
                self.load_configuration()
            )

            runtime = (
                self.load_runtime()
            )

            backup_interval = configuration[
                "backup_interval_hours"
            ]

            last_successful_backup = runtime[
                "last_successful_backup"
            ]

            last_backup_status = runtime[
                "last_backup_status"
            ]

            # Rule 1
            if last_successful_backup is None:

                return Result.success(

                    data={

                        "should_take_backup":
                            True,

                        "reason":
                            "NO_PREVIOUS_BACKUP",

                    }

                )

            # Rule 2
            if last_backup_status == "FAILED":

                return Result.success(

                    data={

                        "should_take_backup":
                            True,

                        "reason":
                            "LAST_BACKUP_FAILED",

                    }

                )

            # Rule 3
            last_backup_datetime = (
                datetime.strptime(

                    last_successful_backup,
                    "%Y-%m-%d %H:%M:%S",

                )
            )

            current_datetime = (
                datetime.now()
            )

            elapsed_hours = (

                current_datetime
                - last_backup_datetime

            ).total_seconds() / 3600

            if elapsed_hours >= backup_interval:

                return Result.success(

                    data={

                        "should_take_backup":
                            True,

                        "reason":
                            "BACKUP_INTERVAL_EXCEEDED",

                    }

                )

            # Rule 4
            return Result.success(

                data={

                    "should_take_backup":
                        False,

                    "reason":
                        "BACKUP_NOT_REQUIRED",

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def update_runtime_information(
        self,
        backup_status,
        duration_seconds=None,
    ):

        try:

            runtime = self.load_runtime()

            current_datetime = (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            if backup_status == "SUCCESS":

                runtime[
                    "last_successful_backup"
                ] = current_datetime

                runtime[
                    "last_backup_status"
                ] = "SUCCESS"

                runtime[
                    "last_backup_duration_seconds"
                ] = duration_seconds

                runtime[
                    "total_successful_backups"
                ] += 1

            elif backup_status == "FAILED":

                runtime[
                    "last_failed_backup"
                ] = current_datetime

                runtime[
                    "last_backup_status"
                ] = "FAILED"

                runtime[
                    "last_backup_duration_seconds"
                ] = None

                runtime[
                    "total_failed_backups"
                ] += 1

            with open(
                "runtime/backup_runtime.json",
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    runtime,
                    file,
                    indent=4,
                )

            return Result.success(
                data=runtime
            )

        except Exception as error:

            return Result.error(
                str(error)
            )