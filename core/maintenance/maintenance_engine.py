from dataclasses import dataclass


@dataclass
class MaintenanceResult:

    success: bool
    message: str
    affected_rows: int = 0


class MaintenanceEngine:

    def __init__(self, database):

        self.database = database

    def execute(self, sql: str) -> MaintenanceResult:

        connection = None
        cursor = None

        try:

            #
            # DBCC SHRINKDATABASE must run outside
            # a user transaction.
            #

            autocommit = "DBCC SHRINKDATABASE" in sql.upper()

            connection = self.database.connect(
                autocommit=autocommit
            )

            cursor = connection.cursor()

            cursor.execute(sql)

            affected_rows = cursor.rowcount

            if not autocommit:

                connection.commit()

            return MaintenanceResult(

                success=True,

                message="Operation completed successfully.",

                affected_rows=affected_rows,

            )

        except Exception as ex:

            if connection and not autocommit:

                connection.rollback()

            return MaintenanceResult(

                success=False,

                message=str(ex),

            )

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()