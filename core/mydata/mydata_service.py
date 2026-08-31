from dataclasses import dataclass
from typing import Callable, Any

import requests

from core.database.database_context import database_context
from core.database.database_connection import DatabaseConnection


@dataclass
class MyDataInvoice:

    invoice_type: str
    document_name: str
    issue_date: str
    aa: str
    invoice_id: int
    cust_afm: str

    sent: bool = False
    send_status: int | None = None
    send_message: str = ""


class MyDataService:

    API_BASE_URL = (
        "http://localhost/External.Tax.Provider"
    )

    SEND_USER_ID = 3

    SEARCH_SQL = """
    SELECT DISTINCT
        CAST(invoiceType AS NVARCHAR(64)) AS InvoiceType,
        CAST(DocumentType AS NVARCHAR(256)) AS DocumentName,
        CONVERT(varchar(10), issueDate, 23) AS IssueDate,
        aa,
        InvoiceId,
        CustAFM
    FROM VSnMyDATAInvoicesAMV
    WHERE CONVERT(date, issueDate)
        BETWEEN CONVERT(date, ?, 112)
        AND CONVERT(date, ?, 112)
    ORDER BY issueDate, aa
    """

    def _get_connection(self):

        udl_path = database_context.active_udl()

        if not udl_path:
            raise RuntimeError(
                "Δεν έχει επιλεγεί βάση δεδομένων."
            )

        database = DatabaseConnection(
            udl_path
        )

        return database.connect()

    def search(
        self,
        start_date: str,
        end_date: str,
    ):

        connection = self._get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                self.SEARCH_SQL,
                start_date,
                end_date,
            )

            rows = cursor.fetchall()

            invoices = []

            for row in rows:

                invoices.append(
                    MyDataInvoice(
                        invoice_type=str(row[0] or ""),
                        document_name=str(row[1] or ""),
                        issue_date=str(row[2] or ""),
                        aa=str(row[3] or ""),
                        invoice_id=int(row[4]),
                        cust_afm=str(row[5] or ""),
                    )
                )

            cursor.close()

            return invoices

        finally:

            connection.close()

    def send_invoice(
        self,
        invoice_id: int,
    ):

        url = (
            f"{self.API_BASE_URL}"
            "/api/TaxProvider/"
            "SendInvoice/1/0/1/1/0"
        )

        params = {
            "id": invoice_id,
            "userId": self.SEND_USER_ID,
        }

        response = requests.post(
            url,
            params=params,
            timeout=120,
        )

        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "message": response.text,
            "url": response.url,
        }

    def send_invoices(
        self,
        invoices,
        progress_callback: Callable[[int, int, Any, str], None] | None = None,
    ):

        results = []
        total = len(invoices)

        for index, invoice in enumerate(
            invoices,
            start=1,
        ):

            if progress_callback:

                progress_callback(
                    index - 1,
                    total,
                    invoice,
                    "sending",
                )

            try:

                result = self.send_invoice(
                    invoice.invoice_id
                )

                invoice.send_status = (
                    result["status_code"]
                )

                invoice.send_message = (
                    result["message"]
                )

                invoice.sent = (
                    result["success"]
                )

                results.append(
                    {
                        "invoice": invoice,
                        "result": result,
                    }
                )

            except Exception as exc:

                invoice.sent = False
                invoice.send_status = None
                invoice.send_message = str(exc)

                result = {
                    "success": False,
                    "status_code": None,
                    "message": str(exc),
                }

                results.append(
                    {
                        "invoice": invoice,
                        "result": result,
                    }
                )

            finally:

                if progress_callback:

                    progress_callback(
                        index,
                        total,
                        invoice,
                        "completed",
                    )

        return results

    def database_selected(self):

        return database_context.is_selected()
