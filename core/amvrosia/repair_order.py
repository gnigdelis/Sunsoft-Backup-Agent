from dataclasses import dataclass


@dataclass
class OrderResult:

    found: bool

    order_number: int = 0

    total_rows: int = 0

    status_0: int = 0

    status_1: int = 0

    status_2: int = 0

    repairable: int = 0

    message: str = ""


@dataclass
class RepairResult:

    success: bool

    order_number: int = 0

    updated_rows: int = 0

    remaining_rows: int = 0

    message: str = ""


class RepairOrder:

    SEARCH_SQL = """
    SELECT
        SalesTransOID,
        SalesTransStatus
    FROM TblSnSalesTrans
    WHERE SalesTransNoteNo = ?
    """

    UPDATE_SQL = """
    UPDATE TblSnSalesTrans
    SET SalesTransStatus = 1
    WHERE SalesTransNoteNo = ?
      AND SalesTransStatus IN (0, 2)
    """

    VERIFY_SQL = """
    SELECT
        SalesTransStatus
    FROM TblSnSalesTrans
    WHERE SalesTransNoteNo = ?
      AND SalesTransStatus IN (0, 2)
    """

    def search(
        self,
        connection,
        order_number: int,
    ) -> OrderResult:

        cursor = connection.cursor()

        try:

            cursor.execute(
                self.SEARCH_SQL,
                order_number,
            )

            rows = cursor.fetchall()

            if not rows:

                return OrderResult(
                    found=False,
                    order_number=order_number,
                    message="Η παραγγελία δεν βρέθηκε.",
                )

            status_0 = 0
            status_1 = 0
            status_2 = 0

            for row in rows:

                status = int(
                    row.SalesTransStatus
                )

                if status == 0:

                    status_0 += 1

                elif status == 1:

                    status_1 += 1

                elif status == 2:

                    status_2 += 1

            repairable = (
                status_0 + status_2
            )

            return OrderResult(
                found=True,
                order_number=order_number,
                total_rows=len(rows),
                status_0=status_0,
                status_1=status_1,
                status_2=status_2,
                repairable=repairable,
                message="Η παραγγελία βρέθηκε.",
            )

        finally:

            cursor.close()

    def repair(
        self,
        connection,
        order_number: int,
    ) -> RepairResult:

        cursor = connection.cursor()

        try:

            cursor.execute(
                self.SEARCH_SQL,
                order_number,
            )

            rows = cursor.fetchall()

            if not rows:

                return RepairResult(
                    success=False,
                    order_number=order_number,
                    message="Η παραγγελία δεν βρέθηκε.",
                )

            repairable = 0

            for row in rows:

                status = int(
                    row.SalesTransStatus
                )

                if status in (0, 2):

                    repairable += 1

            if repairable == 0:

                return RepairResult(
                    success=True,
                    order_number=order_number,
                    updated_rows=0,
                    remaining_rows=0,
                    message=(
                        "Η παραγγελία είναι ήδη "
                        "ολοκληρωμένη."
                    ),
                )

            cursor.execute(
                self.UPDATE_SQL,
                order_number,
            )

            updated_rows = cursor.rowcount

            connection.commit()

            cursor.execute(
                self.VERIFY_SQL,
                order_number,
            )

            remaining = cursor.fetchall()

            remaining_rows = len(remaining)

            if remaining_rows > 0:

                connection.rollback()

                return RepairResult(
                    success=False,
                    order_number=order_number,
                    updated_rows=updated_rows,
                    remaining_rows=remaining_rows,
                    message=(
                        "Η διόρθωση δεν ολοκληρώθηκε. "
                        f"Παραμένουν {remaining_rows} "
                        "γραμμές με Status 0 ή 2."
                    ),
                )

            return RepairResult(
                success=True,
                order_number=order_number,
                updated_rows=updated_rows,
                remaining_rows=0,
                message=(
                    "Η παραγγελία διορθώθηκε "
                    "επιτυχώς."
                ),
            )

        except Exception:

            connection.rollback()

            raise

        finally:

            cursor.close()