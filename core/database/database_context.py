from PySide6.QtCore import QObject, Signal

from core.configuration.udl_locator import UDLLocator
from core.database.udl_reader import UDLReader


class DatabaseContext(QObject):

    database_changed = Signal(object)

    def __init__(self):

        super().__init__()

        self._active_udl = None

    def available_databases(self):

        databases = []

        for udl_path in UDLLocator.find_all():

            try:

                reader = UDLReader(
                    udl_path
                )

                databases.append(
                    {
                        "path": str(udl_path),
                        "name": reader.get_database_name(),
                        "server": reader.get_server_name(),
                    }
                )

            except Exception:
                continue

        return databases

    def select(self, udl_path):

        reader = UDLReader(
            udl_path
        )

        database = {
            "path": str(udl_path),
            "name": reader.get_database_name(),
            "server": reader.get_server_name(),
        }

        self._active_udl = database

        self.database_changed.emit(
            database
        )

        return database

    def active(self):

        return self._active_udl

    def active_udl(self):

        if not self._active_udl:

            return None

        return self._active_udl["path"]

    def is_selected(self):

        return self._active_udl is not None


database_context = DatabaseContext()