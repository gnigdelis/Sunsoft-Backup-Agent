from core.configuration.udl_locator import (
    UDLLocator,
)

from core.database.database_connection import (
    DatabaseConnection,
)

from core.amvrosia.repair_order import (
    RepairOrder,
)


class AmvrosiaService:

    def __init__(self):

        udl_path = UDLLocator.find()

        self.database = DatabaseConnection(
            udl_path
        )

        self.repair = RepairOrder()

    def search_order(
        self,
        order_number: int,
    ):

        connection = self.database.connect()

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

        connection = self.database.connect()

        try:

            return self.repair.repair(
                connection,
                order_number,
            )

        finally:

            connection.close()


amvrosia_service = AmvrosiaService()