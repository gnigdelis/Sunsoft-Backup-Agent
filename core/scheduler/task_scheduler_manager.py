import subprocess

from core.common.result import Result


class TaskSchedulerManager:

    TASK_NAME = "Sunsoft Guardian Policy Engine"

    def task_exists(self):

        try:

            result = subprocess.run(
                [
                    "schtasks",
                    "/Query",
                    "/TN",
                    self.TASK_NAME,
                ],
                capture_output=True,
                text=True,
            )

            return Result.success(
                data={
                    "task_name": self.TASK_NAME,
                    "exists": result.returncode == 0,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def create_policy_task(self):

        try:

            result = subprocess.run(
                [
                    "schtasks",
                    "/Create",
                    "/SC",
                    "HOURLY",
                    "/MO",
                    "1",
                    "/TN",
                    self.TASK_NAME,
                    "/TR",
                    "cmd.exe /c exit",
                    "/F",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:

                return Result.error(
                    result.stderr
                )

            return Result.success(
                data={
                    "task_name": self.TASK_NAME,
                    "created": True,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def delete_policy_task(self):

        try:

            result = subprocess.run(
                [
                    "schtasks",
                    "/Delete",
                    "/TN",
                    self.TASK_NAME,
                    "/F",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:

                return Result.error(
                    result.stderr
                )

            return Result.success(
                data={
                    "task_name": self.TASK_NAME,
                    "deleted": True,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )