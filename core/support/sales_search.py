from dataclasses import dataclass


@dataclass
class SalesSearchResult:

    found: bool

    rows: list[dict]

    total_records: int

    pending_records: int

    message: str = ""


class SalesSearch:

    SQL = """
    SELECT
        SalesTransOID,
        SalesTransStatus,
        SalesTransNoteNo,
        SalesTransNoteCode,
        SalesTransInitDate
    FROM TblSnSalesTrans
    WHERE SalesTransNoteNo = ?
      AND SalesTransInitDate = ?
    ORDER BY SalesTransOID
    """

    def execute(
        self,
        connection,
        order_number: int,
        order_date: str,
    ) -> SalesSearchResult:

        cursor = connection.cursor()

        try:

            cursor.execute(
                self.SQL,
                order_number,
                order_date,
            )

            rows = cursor.fetchall()

            if not rows:

                return SalesSearchResult(
                    found=False,
                    rows=[],
                    total_records=0,
                    pending_records=0,
                    message="Order not found.",
                )

            result_rows = []

            pending_count = 0

            for row in rows:

                oid = row[0]
                status = row[1]
                note_no = row[2]
                note_code = row[3]
                init_date = row[4]

                try:

                    oid = int(
                        oid
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    oid = None

                try:

                    status = int(
                        status
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    status = None

                if status != 1:

                    pending_count += 1

                result_rows.append(
                    {
                        "SalesTransOID": oid,
                        "SalesTransStatus": status,
                        "SalesTransNoteNo": note_no,
                        "SalesTransNoteCode": note_code,
                        "SalesTransInitDate": init_date,
                    }
                )

            return SalesSearchResult(
                found=True,
                rows=result_rows,
                total_records=len(
                    result_rows
                ),
                pending_records=pending_count,
                message="Order found.",
            )

        except Exception as error:

            return SalesSearchResult(
                found=False,
                rows=[],
                total_records=0,
                pending_records=0,
                message=str(
                    error
                ),
            )

        finally:

            cursor.close()