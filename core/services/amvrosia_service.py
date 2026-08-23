from core.database.database_context import database_context
from core.database.database_connection import DatabaseConnection

from core.amvrosia.repair_order import (
    RepairOrder,
)


class AmvrosiaService:

    def __init__(self):

        self.database = None

        self.repair = RepairOrder()

    def _get_database(self):

        udl_path = database_context.active_udl()

        if not udl_path:

            raise RuntimeError(
                "No database selected."
            )

        return DatabaseConnection(
            udl_path
        )

    def search_order(
        self,
        order_number: int,
    ):

        database = self._get_database()

        connection = database.connect()

        try:

            return self.repair.search(
                connection,
                order_number,
            )

        finally:

            connection.close()

    def repair_order(
        self,
        order_number: int,
    ):

        database = self._get_database()

        connection = database.connect()

        try:

            return self.repair.repair(
                connection,
                order_number,
            )

        finally:

            connection.close()


amvrosia_service = AmvrosiaService()
