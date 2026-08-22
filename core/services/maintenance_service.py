from core.database.database_context import database_context
from core.database.database_connection import DatabaseConnection

from core.maintenance.maintenance_engine import MaintenanceEngine

from core.maintenance.delete_mydata_response import (
    DeleteMyDataResponse,
)

from core.maintenance.rebuild_database import (
    RebuildDatabase,
)

from core.maintenance.shrink_database import (
    ShrinkDatabase,
)


class MaintenanceService:
    """
    Shared Database Maintenance Service.

    Uses the UDL selected in database_context.
    """

    def _get_database(self):

        udl_path = database_context.active_udl()

        if not udl_path:

            raise RuntimeError(
                "No database selected."
            )

        return DatabaseConnection(
            udl_path
        )

    def _execute_step(
        self,
        step,
    ):

        database = self._get_database()

        engine = MaintenanceEngine(
            database
        )

        result = engine.execute(
            step.get_sql()
        )

        return {
            "step": step.name,
            "success": result.success,
            "message": result.message,
            "affected_rows": result.affected_rows,
        }

    # ==========================================================
    # Delete MyDATA Response
    # ==========================================================

    def delete_mydata(self):

        return self._execute_step(
            DeleteMyDataResponse()
        )

    # ==========================================================
    # Rebuild Database
    # ==========================================================

    def rebuild(self):

        return self._execute_step(
            RebuildDatabase()
        )

    # ==========================================================
    # Shrink Database
    # ==========================================================

    def shrink(self):

        return self._execute_step(
            ShrinkDatabase()
        )

    # ==========================================================
    # Legacy Full Maintenance
    # ==========================================================

    def run(self):

        results = []

        steps = [
            DeleteMyDataResponse(),
            RebuildDatabase(),
            ShrinkDatabase(),
        ]

        for step in steps:

            result = self._execute_step(
                step
            )

            results.append(
                result
            )

            if not result["success"]:

                break

        return results


maintenance_service = MaintenanceService()