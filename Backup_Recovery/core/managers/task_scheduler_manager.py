import subprocess
import csv
import io


class TaskSchedulerManager:

    def __init__(self):

        pass

    def get_scheduled_tasks(self):

        tasks = []

        try:

            result = subprocess.run(

                [

                    "schtasks",
                    "/query",
                    "/fo",
                    "csv",
                    "/v"

                ],

                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"

            )

            reader = csv.DictReader(

                io.StringIO(
                    result.stdout
                )

            )

            for row in reader:

                tasks.append(

                    {

                        "task_name":
                            row.get(
                                "TaskName",
                                "",
                            ),

                        "status":
                            row.get(
                                "Status",
                                "",
                            ),

                        "author":
                            row.get(
                                "Author",
                                "",
                            ),

                        "next_run_time":
                            row.get(
                                "Next Run Time",
                                "",
                            ),

                        "last_run_time":
                            row.get(
                                "Last Run Time",
                                "",
                            ),

                    }

                )

        except Exception:

            pass

        return tasks

    def get_information(self):

        tasks = self.get_scheduled_tasks()

        warnings = []

        status = "SUCCESS"

        if len(tasks) == 0:

            status = "WARNING"

            warnings.append(

                "No scheduled tasks found."

            )

        return {

            "success": True,

            "status": status,

            "warnings": warnings,

            "errors": [],

            "data": tasks,

        }