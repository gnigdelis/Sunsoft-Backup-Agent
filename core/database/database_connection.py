import pyodbc

from core.database.udl_reader import UDLReader


class DatabaseConnection:

    def __init__(self, udl_path: str):

        self.reader = UDLReader(udl_path)

        self.connection_string = (
            self.reader.get_connection_string()
        )

    def connect(
        self,
        autocommit: bool = False,
    ):

        return pyodbc.connect(

            self.connection_string,

            autocommit=autocommit,

        )

    def server_name(self):

        return self.reader.get_server_name()

    def database_name(self):

        return self.reader.get_database_name()