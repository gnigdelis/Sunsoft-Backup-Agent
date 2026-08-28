from dataclasses import dataclass
import re
import threading


@dataclass
class MaintenanceResult:

    success: bool
    message: str
    affected_rows: int = 0


class MaintenanceEngine:

    TABLE_PROGRESS_PATTERN = re.compile(
        r"\bTable\s+(\d+)\s+of\s+(\d+)\b",
        re.IGNORECASE,
    )

    ODBC_PREFIX_PATTERN = re.compile(
        r"^\[Microsoft\]\[ODBC Driver [^\]]+\]\[SQL Server\]",
        re.IGNORECASE,
    )

    def __init__(self, database):

        self.database = database

        self.connection = None
        self.cursor = None

        self._cancel_requested = threading.Event()

    def request_cancel(self):

        self._cancel_requested.set()

        connection = self.connection

        if connection is None:
            return

        cursor = self.cursor

        if cursor is not None:

            try:
                cursor.cancel()
            except Exception:
                pass

    def execute(
        self,
        sql: str,
        progress_callback=None,
    ) -> MaintenanceResult:

        connection = None
        cursor = None

        autocommit = (
            "DBCC SHRINKDATABASE" in sql.upper()
        )

        self._cancel_requested.clear()

        try:

            connection = self.database.connect(
                autocommit=autocommit
            )

            self.connection = connection

            cursor = connection.cursor()

            self.cursor = cursor

            if self._cancel_requested.is_set():

                return MaintenanceResult(
                    success=False,
                    message="Operation cancelled by user.",
                    affected_rows=0,
                )

            cursor.execute(sql)

            affected_rows = cursor.rowcount

            while True:

                if self._cancel_requested.is_set():

                    return MaintenanceResult(
                        success=False,
                        message="Operation cancelled by user.",
                        affected_rows=0,
                    )

                self._process_messages(
                    cursor,
                    progress_callback,
                )

                if cursor.description:

                    while cursor.fetchone() is not None:

                        if self._cancel_requested.is_set():

                            return MaintenanceResult(
                                success=False,
                                message=(
                                    "Operation cancelled by user."
                                ),
                                affected_rows=0,
                            )

                try:

                    has_next = cursor.nextset()

                except Exception:

                    has_next = False

                if not has_next:

                    break

                if cursor.rowcount not in (
                    None,
                    -1,
                ):

                    affected_rows = cursor.rowcount

            self._process_messages(
                cursor,
                progress_callback,
            )

            if self._cancel_requested.is_set():

                return MaintenanceResult(
                    success=False,
                    message="Operation cancelled by user.",
                    affected_rows=0,
                )

            if not autocommit:

                connection.commit()

            if affected_rows is None:

                affected_rows = 0

            if progress_callback:

                progress_callback(
                    100,
                    "Operation completed.",
                )

            return MaintenanceResult(

                success=True,

                message=(
                    "Operation completed successfully."
                ),

                affected_rows=affected_rows,

            )

        except Exception as ex:

            if self._cancel_requested.is_set():

                return MaintenanceResult(

                    success=False,

                    message=(
                        "Operation cancelled by user."
                    ),

                    affected_rows=0,

                )

            if connection and not autocommit:

                try:
                    connection.rollback()
                except Exception:
                    pass

            return MaintenanceResult(

                success=False,

                message=str(ex),

                affected_rows=0,

            )

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:

                try:
                    connection.close()
                except Exception:
                    pass

            self.cursor = None
            self.connection = None

    def _clean_sql_server_message(
        self,
        message,
    ):

        text = str(
            message
        ).strip()

        text = self.ODBC_PREFIX_PATTERN.sub(
            "",
            text,
        ).strip()

        table_match = self.TABLE_PROGRESS_PATTERN.search(
            text
        )

        if table_match:

            text = text[
                table_match.start():
            ].strip()

        return text

    def _process_messages(
        self,
        cursor,
        progress_callback,
    ):

        if not progress_callback:
            return

        messages = getattr(
            cursor,
            "messages",
            [],
        )

        for _, message in messages:

            text = self._clean_sql_server_message(
                message
            )

            match = (
                self.TABLE_PROGRESS_PATTERN.search(
                    text
                )
            )

            if not match:
                continue

            current = int(
                match.group(1)
            )

            total = int(
                match.group(2)
            )

            if total <= 0:
                continue

            current = max(
                0,
                min(
                    current,
                    total,
                ),
            )

            percent = int(
                round(
                    current * 100 / total
                )
            )

            progress_callback(
                percent,
                text,
            )