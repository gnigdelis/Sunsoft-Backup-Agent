from core.database.database_context import database_context
from core.database.database_connection import DatabaseConnection

from core.support.sales_search import SalesSearch
from core.support.sales_status_reset import SalesStatusReset


class SupportService:

    def __init__(self):

        self.database = None

        self.search_service = SalesSearch()

        self.reset_service = SalesStatusReset()

    def _get_database(self):

        udl_path = database_context.active_udl()

        if not udl_path:

            raise RuntimeError(
                "No database selected."
            )

        return DatabaseConnection(
            udl_path
        )

    def search_invoice(
        self,
        invoice_number: int,
        invoice_date: str,
    ):

        database = self._get_database()

        connection = database.connect()

        try:

            return self.search_service.execute(

                connection,

                invoice_number,

                invoice_date,

            )

        finally:

            connection.close()

    def reset_status(
        self,
        oid: int,
    ):

        database = self._get_database()

        connection = database.connect()

        try:

            return self.reset_service.by_oid(

                connection,

                oid,

            )

        finally:

            connection.close()

    def reset_status_range(
        self,
        start_oid: int,
        end_oid: int,
    ):

        database = self._get_database()

        connection = database.connect()

        try:

            return self.reset_service.by_range(

                connection,

                start_oid,

                end_oid,

            )

        finally:

            connection.close()
