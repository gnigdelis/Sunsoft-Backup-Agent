from core.maintenance.delete_mydata_response import (
    DeleteMyDataResponse,
)

from core.maintenance.rebuild_database import (
    RebuildDatabase,
)

from core.maintenance.shrink_database import (
    ShrinkDatabase,
)


class MaintenancePipeline:

    def __init__(self, engine):

        self.engine = engine

        self.steps = {

            "delete": DeleteMyDataResponse(),

            "rebuild": RebuildDatabase(),

            "shrink": ShrinkDatabase(),

        }

    def execute_step(self, step_key):

        step = self.steps.get(step_key)

        if not step:

            return {
                "step": step_key,
                "success": False,
                "message": "Unknown maintenance operation.",
                "affected_rows": 0,
            }

        result = self.engine.execute(
            step.get_sql()
        )

        return {
            "step": step.name,
            "success": result.success,
            "message": result.message,
            "affected_rows": result.affected_rows,
        }

    def execute(self):

        results = []

        for step_key in (
            "delete",
            "rebuild",
            "shrink",
        ):

            result = self.execute_step(
                step_key
            )

            results.append(result)

            if not result["success"]:
                break

        return results