from dataclasses import dataclass


@dataclass
class SalesStatusResetResult:

    success: bool
    affected_rows: int = 0
    message: str = ""


class SalesStatusReset:

    SQL_BY_OID = """
    UPDATE TblSnSalesTrans
    SET SalesTransStatus = 1
    WHERE SalesTransOID = ?
    """

    SQL_BY_RANGE = """
    UPDATE TblSnSalesTrans
    SET SalesTransStatus = 1
    WHERE SalesTransOID BETWEEN ? AND ?
    """

    def by_oid(
        self,
        connection,
        oid: int,
    ) -> SalesStatusResetResult:

        cursor = connection.cursor()

        cursor.execute(
            self.SQL_BY_OID,
            oid,
        )

        affected = cursor.rowcount

        connection.commit()

        cursor.close()

        return SalesStatusResetResult(

            success=True,

            affected_rows=affected,

            message="Status updated successfully.",

        )

    def by_range(
        self,
        connection,
        start_oid: int,
        end_oid: int,
    ) -> SalesStatusResetResult:

        cursor = connection.cursor()

        cursor.execute(

            self.SQL_BY_RANGE,

            start_oid,

            end_oid,

        )

        affected = cursor.rowcount

        connection.commit()

        cursor.close()

        return SalesStatusResetResult(

            success=True,

            affected_rows=affected,

            message="Statuses updated successfully.",

        )