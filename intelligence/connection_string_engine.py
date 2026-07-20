from core.database_snapshot import DatabaseSnapshot


def discover_connection_strings(
    parser_results
) -> list[DatabaseSnapshot]:
    """
    Discovers database connection strings
    from parsed configuration files.
    """

    databases = []

    #
    # TODO:
    #
    # - SQL Server connection strings
    # - PostgreSQL connection strings
    # - SQLite connection strings
    # - Future database providers
    #

    return databases