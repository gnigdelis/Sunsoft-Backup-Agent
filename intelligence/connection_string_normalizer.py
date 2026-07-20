def normalize_connection_string(
    data: dict
) -> dict:
    """
    Normalizes connection string keys.

    Supported formats:

    Server
    Data Source
    Host

    Initial Catalog
    Database

    User ID
    UID
    Username

    Password
    PWD

    Port

    Returns a normalized dictionary.
    """

    normalized = {

        "server": "",
        "database_name": "",
        "username": "",
        "password": "",
        "port": "",

    }

    #
    # SERVER
    #

    if "server" in data:
        normalized["server"] = data["server"]

    elif "data source" in data:
        normalized["server"] = data["data source"]

    elif "host" in data:
        normalized["server"] = data["host"]

    #
    # DATABASE NAME
    #

    if "initial catalog" in data:
        normalized["database_name"] = (
            data["initial catalog"]
        )

    elif "database" in data:
        normalized["database_name"] = (
            data["database"]
        )

    #
    # USERNAME
    #

    if "user id" in data:
        normalized["username"] = (
            data["user id"]
        )

    elif "uid" in data:
        normalized["username"] = (
            data["uid"]
        )

    elif "username" in data:
        normalized["username"] = (
            data["username"]
        )

    #
    # PASSWORD
    #

    if "password" in data:
        normalized["password"] = (
            data["password"]
        )

    elif "pwd" in data:
        normalized["password"] = (
            data["pwd"]
        )

    #
    # PORT
    #

    if "port" in data:
        normalized["port"] = (
            data["port"]
        )

    #
    # SQL SERVER PORT
    #
    # Example:
    #
    # Server=10.10.241.79,1433
    #

    if "," in normalized["server"]:

        values = (
            normalized["server"]
            .split(",")
        )

        if len(values) == 2:

            normalized["server"] = (
                values[0]
                .strip()
            )

            normalized["port"] = (
                values[1]
                .strip()
            )

    return normalized