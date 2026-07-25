import subprocess

from core.common.result import Result


class ScheduleManager:

    TASK_NAME = "Sunsoft Backup Agent"

    def create_daily_schedule(
        self,
        time,
        executable_path,
    ):

        try:

            command = [
                "schtasks",
                "/Create",
                "/TN",
                self.TASK_NAME,
                "/SC",
                "DAILY",
                "/ST",
                time,
                "/TR",
                f'"{executable_path}" --silent',
                "/F",
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def delete_schedule(self):

        try:

            command = [
                "schtasks",
                "/Delete",
                "/TN",
                self.TASK_NAME,
                "/F",
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def get_schedule_status(self):

        try:

            command = [
                "schtasks",
                "/Query",
                "/TN",
                self.TASK_NAME,
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )