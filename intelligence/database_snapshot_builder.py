from core.database_snapshot import (
    DatabaseSnapshot,
)


def build_database_snapshot(
    data: dict
) -> DatabaseSnapshot:

    return DatabaseSnapshot(

        server=data.get(
            "server",
            ""
        ),

        database_name=data.get(
            "database_name",
            ""
        ),

        username=data.get(
            "username",
            ""
        ),

        password=data.get(
            "password",
            ""
        ),

        port=data.get(
            "port",
            ""
        ),

    )