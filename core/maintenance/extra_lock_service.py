from dataclasses import dataclass

from core.database.database_context import database_context
from core.database.database_connection import DatabaseConnection


@dataclass
class ExtraLockItem:
    name: str
    value: int


class ExtraLockService:

    SELECT_SQL = """
    SELECT
        AppInfoExtraLock
    FROM TblSnAppInfo
    """

    UPDATE_SQL = """
    UPDATE TblSnAppInfo
    SET AppInfoExtraLock = ?
    """

    DEFAULT_ITEMS = [
        "Tables",
        "Kitchen",
        "Cashier",
        "Delivery",
        "PostPos",
        "PrintSrv",
        "KDSi",
        "ARS",
        "Orderman",
        "Pocket",
        "BCS",
        "Maps",
        "Android",
        "External",
    ]

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

    def _normalize_raw_value(
        self,
        value,
    ):

        if value is None:
            return ""

        if isinstance(
            value,
            (bytes, bytearray),
        ):

            value = value.decode(
                "utf-8",
                errors="ignore",
            )

        return str(
            value
        ).strip()

    def load(self):

        connection = self._get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                self.SELECT_SQL
            )

            rows = cursor.fetchall()

            cursor.close()

            raw_value = ""

            #
            # Find the first real ExtraLock value.
            #

            for row in rows:

                if not row:
                    continue

                candidate = (
                    self._normalize_raw_value(
                        row[0]
                    )
                )

                if candidate:

                    raw_value = candidate

                    break

            if not raw_value:

                raise RuntimeError(
                    "Το AppInfoExtraLock είναι κενό "
                    "στην TblSnAppInfo."
                )

            #
            # Expected format:
            #
            # 1;1;1;1;0;1;0;1;0;0;0;0;4;0
            #

            values = [
                value.strip()
                for value in raw_value.split(";")
            ]

            if len(values) < len(
                self.DEFAULT_ITEMS
            ):

                raise RuntimeError(
                    "Το AppInfoExtraLock περιέχει "
                    f"{len(values)} τιμές αντί για "
                    f"{len(self.DEFAULT_ITEMS)}."
                )

            items = []

            for index, name in enumerate(
                self.DEFAULT_ITEMS
            ):

                try:

                    value = int(
                        values[index]
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    raise RuntimeError(
                        "Μη έγκυρη τιμή στο "
                        f"AppInfoExtraLock στη θέση "
                        f"{index + 1}: "
                        f"{values[index]}"
                    )

                items.append(
                    ExtraLockItem(
                        name=name,
                        value=value,
                    )
                )

            return {
                "raw": raw_value,
                "items": items,
            }

        finally:

            connection.close()

    def save(
        self,
        values,
    ):

        if len(values) != len(
            self.DEFAULT_ITEMS
        ):

            raise ValueError(
                "Μη έγκυρος αριθμός επιλογών."
            )

        normalized = []

        for value in values:

            try:

                number = int(
                    value
                )

            except (
                TypeError,
                ValueError,
            ):

                raise ValueError(
                    "Οι τιμές πρέπει να είναι αριθμοί."
                )

            if number < 0:

                raise ValueError(
                    "Οι τιμές δεν μπορούν "
                    "να είναι αρνητικές."
                )

            normalized.append(
                str(number)
            )

        extra_lock = ";".join(
            normalized
        )

        connection = self._get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                self.UPDATE_SQL,
                extra_lock,
            )

            affected_rows = (
                cursor.rowcount
            )

            if affected_rows <= 0:

                connection.rollback()

                raise RuntimeError(
                    "Δεν ενημερώθηκε η "
                    "TblSnAppInfo."
                )

            connection.commit()

            return {
                "success": True,
                "value": extra_lock,
                "affected_rows": affected_rows,
            }

        except Exception:

            connection.rollback()

            raise

        finally:

            cursor.close()
            connection.close()


extra_lock_service = ExtraLockService()