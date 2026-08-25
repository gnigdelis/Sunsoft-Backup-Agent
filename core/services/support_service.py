from core.database.database_context import database_context
from core.database.database_connection import DatabaseConnection

from core.support.sales_search import SalesSearch
from core.support.sales_status_reset import SalesStatusReset


class SupportService:

    def __init__(self):

        self.database = None

        self.search_service = (
            SalesSearch()
        )

        self.reset_service = (
            SalesStatusReset()
        )

    # ==========================================================
    # DATABASE
    # ==========================================================

    def _get_database(self):

        udl_path = (
            database_context.active_udl()
        )

        if not udl_path:

            raise RuntimeError(
                "No database selected."
            )

        return DatabaseConnection(
            udl_path
        )

    # ==========================================================
    # SEARCH ORDER
    # ==========================================================

    def search_invoice(
        self,
        invoice_number: int,
        invoice_date: str,
    ):

        database = (
            self._get_database()
        )

        connection = (
            database.connect()
        )

        try:

            return self.search_service.execute(
                connection,
                invoice_number,
                invoice_date,
            )

        finally:

            connection.close()

    # ==========================================================
    # CLOSE PENDING ORDER
    #
    # Business rule:
    #
    # SalesTransStatus = 1
    #     -> already closed
    #
    # SalesTransStatus <> 1
    #     -> pending/open
    #
    # All pending records of the selected order
    # are changed to status 1.
    # ==========================================================

    def close_pending_order(
        self,
        order_number: int,
        order_date: str,
    ):

        database = (
            self._get_database()
        )

        connection = (
            database.connect()
        )

        cursor = connection.cursor()

        sql = """
        UPDATE TblSnSalesTrans
        SET SalesTransStatus = 1
        WHERE SalesTransNoteNo = ?
          AND SalesTransInitDate = ?
          AND SalesTransStatus <> 1
        """

        try:

            cursor.execute(
                sql,
                order_number,
                order_date,
            )

            affected_rows = (
                cursor.rowcount
            )

            connection.commit()

            return {
                "success": True,
                "affected_rows": affected_rows,
                "message": (
                    f"{affected_rows} "
                    "pending record(s) closed."
                ),
            }

        except Exception as error:

            connection.rollback()

            return {
                "success": False,
                "affected_rows": 0,
                "message": str(
                    error
                ),
            }

        finally:

            cursor.close()
            connection.close()

    # ==========================================================
    # LEGACY SINGLE OID RESET
    # ==========================================================

    def reset_status(
        self,
        oid: int,
    ):

        database = (
            self._get_database()
        )

        connection = (
            database.connect()
        )

        try:

            return self.reset_service.by_oid(
                connection,
                oid,
            )

        finally:

            connection.close()

    # ==========================================================
    # LEGACY OID RANGE RESET
    # ==========================================================

    def reset_status_range(
        self,
        start_oid: int,
        end_oid: int,
    ):

        database = (
            self._get_database()
        )

        connection = (
            database.connect()
        )

        try:

            return self.reset_service.by_range(
                connection,
                start_oid,
                end_oid,
            )

        finally:

            connection.close()