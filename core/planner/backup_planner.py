import json

from core.common.result import Result


class BackupPlanner:

    def __init__(self):

        self.included_targets = []

        self.skipped_targets = []

        self.warnings = []

        self.recommendations = []

        self.ready_to_collect = True

        self.settings = self.load_settings()

    def load_settings(self):

        with open(

            "settings/backup/backup_targets.json",
            "r",
            encoding="utf-8",

        ) as file:

            return json.load(
                file
            )

    def include_target(

        self,
        target_name,

    ):

        self.included_targets.append(
            target_name
        )

    def skip_target(

        self,
        target_name,
        warning=None,

    ):

        self.skipped_targets.append(
            target_name
        )

        if warning:

            self.warnings.append(
                warning
            )

    def add_recommendation(

        self,
        message,

    ):

        self.recommendations.append(
            message
        )

    def set_not_ready(self):

        self.ready_to_collect = False

    def get_result(self):

        return Result.success(

            data={

                "ready_to_collect":

                    self.ready_to_collect,

                "included_targets":

                    self.included_targets,

                "skipped_targets":

                    self.skipped_targets,

                "critical_targets":

                    self.settings[
                        "critical_targets"
                    ],

                "warnings":

                    self.warnings,

                "recommendations":

                    self.recommendations,

            }

        )