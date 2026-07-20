def parse_connection_string(
    connection_string: str
) -> dict:
    """
    Parses a connection string into a dictionary.

    Example:

    Server=SQL01;
    Database=DEMO;
    User ID=sa;
    Password=123;

    Returns:

    {
        "server": "SQL01",
        "database": "DEMO",
        "user id": "sa",
        "password": "123"
    }
    """

    result = {}

    if not connection_string:
        return result

    values = connection_string.split(";")

    for value in values:

        value = value.strip()

        if not value:
            continue

        if "=" not in value:
            continue

        key, data = value.split(
            "=",
            maxsplit=1
        )

        key = key.strip().lower()
        data = data.strip()

        result[key] = data

    return result