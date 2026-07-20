KEYWORDS = [

    "server=",
    "database=",
    "initial catalog=",
    "data source=",
    "user id=",
    "uid=",
    "password=",
    "pwd=",
    "host=",
    "port=",

]


def contains_connection_string(
    text: str
) -> bool:

    if not text:
        return False

    text = text.lower()

    for keyword in KEYWORDS:

        if keyword in text:

            return True

    return False