from core.database_snapshot import DatabaseSnapshot

from intelligence.keyword_discovery import (
    contains_connection_string,
)

from intelligence.connection_string_parser import (
    parse_connection_string,
)

from intelligence.connection_string_normalizer import (
    normalize_connection_string,
)

from intelligence.database_snapshot_builder import (
    build_database_snapshot,
)


def discover_database_snapshots(
    connection_string: str
) -> list[DatabaseSnapshot]:

    databases = []

    #
    # Connection String Found?
    #

    if not contains_connection_string(
        connection_string
    ):
        return databases

    #
    # Parse Connection String
    #

    parsed_data = parse_connection_string(
        connection_string
    )

    #
    # Normalize Data
    #

    normalized_data = (
        normalize_connection_string(
            parsed_data
        )
    )

    #
    # Build Database Snapshot
    #

    database = (
        build_database_snapshot(
            normalized_data
        )
    )

    #
    # Ignore empty databases
    #

    if not database.server:
        return databases

    databases.append(database)

    return databases