from core.configuration.udl_locator import UDLLocator
from core.database.database_connection import DatabaseConnection

from core.support.sales_search import SalesSearch
from core.support.sales_status_reset import SalesStatusReset


class SupportService:

    def __init__(self):

        udl_path = UDLLocator.find()

        self.database = DatabaseConnection(
            udl_path
        )

        self.search_service = SalesSearch()

        self.reset_service = SalesStatusReset()

    def search_invoice(
        self,
        invoice_number: int,
        invoice_date: str,
    ):

        connection = self.database.connect()

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

        connection = self.database.connect()

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

        connection = self.database.connect()

        try:

            return self.reset_service.by_range(
                connection,
                start_oid,
                end_oid,
            )

        finally:

            connection.close()


support_service = SupportService()