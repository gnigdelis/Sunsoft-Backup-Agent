from core.common.result import Result
from core.policy.backup_policy_manager import (
    BackupPolicyManager,
)
from core.health.health_check_manager import (
    HealthCheckManager,
)
from core.planner.backup_planner import (
    BackupPlanner,
)


class GuardianEngine:

    def __init__(self):

        self.policy_manager = (
            BackupPolicyManager()
        )

        self.health_manager = (
            HealthCheckManager()
        )

        self.backup_planner = (
            BackupPlanner()
        )

    def start(self):

        try:

            policy_result = (
                self.policy_manager.should_take_backup()
            )

            if not policy_result["success"]:

                return policy_result

            if not policy_result["data"][
                "should_take_backup"
            ]:

                return Result.success(

                    data={

                        "backup_required":
                            False,

                        "message":
                            "Backup is not required."

                    }

                )

            return self.run_backup_pipeline()

        except Exception as error:

            return Result.error(
                str(error)
            )

    def run_backup_pipeline(self):

        try:

            health_result = (
                self.health_manager.run()
            )

            planner_result = (
                self.backup_planner.plan_backup()
            )

            return Result.success(

                data={

                    "backup_required":
                        True,

                    "health_checks":
                        health_result,

                    "backup_plan":
                        planner_result,

                    "message":
                        "Guardian backup pipeline executed successfully.",

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )