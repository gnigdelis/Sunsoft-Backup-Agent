from intelligence.connection_string_discovery import (
    discover_database_snapshots,
)


connection_string = """
Server=10.10.241.79,1433;
Initial Catalog=ExternalConnectionWebApi;
User ID=sa;
Password=123456;
"""


databases = (
    discover_database_snapshots(
        connection_string
    )
)


print()
print("=" * 60)
print("CONNECTION STRING DISCOVERY")
print("=" * 60)
print()

print(
    f"Databases Found : {len(databases)}"
)

print()

for database in databases:

    print(database)
    print()
