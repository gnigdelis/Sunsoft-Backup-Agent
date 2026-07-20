from intelligence.connection_string_engine import (
    discover_connection_strings,
)


print()
print("=" * 60)
print("CONNECTION STRING ENGINE")
print("=" * 60)
print()

databases = discover_connection_strings([])

print(
    f"Databases Found : {len(databases)}"
)

print()