from dataclasses import dataclass


@dataclass
class SalesSearchResult:

    found: bool
    oid: int | None = None
    status: int | None = None
    data: dict | None = None
    message: str = ""


class SalesSearch:

    SQL = """
    SELECT
        SalesTransOID,
        SalesTransStatus,
        *
    FROM TblSnSalesTrans
    WHERE SalesTransNoteNo = ?
      AND SalesTransInitDate = ?
    """

    def execute(
        self,
        connection,
        invoice_number: int,
        invoice_date: str,
    ) -> SalesSearchResult:

        cursor = connection.cursor()

        cursor.execute(

            self.SQL,

            invoice_number,

            invoice_date,

        )

        row = cursor.fetchone()

        cursor.close()

        if row is None:

            return SalesSearchResult(

                found=False,

                message="Invoice not found.",

            )

        columns = [

            column[0]

            for column in cursor.description

        ]

        data = dict(

            zip(

                columns,

                row,

            )

        )

        return SalesSearchResult(

            found=True,

            oid=data["SalesTransOID"],

            status=data["SalesTransStatus"],

            data=data,

            message="Invoice found.",

        )