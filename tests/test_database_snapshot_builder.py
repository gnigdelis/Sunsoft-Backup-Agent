from intelligence.database_snapshot_builder import (
    build_database_snapshot,
)

from intelligence.connection_string_normalizer import (
    normalize_connection_string,
)

from intelligence.connection_string_parser import (
    parse_connection_string,
)


connection_string = """
Server=10.10.241.79,1433;
Initial Catalog=ExternalConnectionWebApi;
User ID=sa;
Password=123456;
"""


parsed_data = (
    parse_connection_string(
        connection_string
    )
)


normalized_data = (
    normalize_connection_string(
        parsed_data
    )
)


database = (
    build_database_snapshot(
        normalized_data
    )
)


print()
print("=" * 60)
print("DATABASE SNAPSHOT BUILDER")
print("=" * 60)
print()

print(database)
print()