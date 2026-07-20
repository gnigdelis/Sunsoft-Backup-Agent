from dataclasses import dataclass


@dataclass
class DatabaseSnapshot:

    server: str = ""

    database_name: str = ""

    username: str = ""

    password: str = ""

    port: str = ""

    connection_string: str = ""

    source_module: str = ""