from intelligence.keyword_discovery import (
    contains_connection_string,
)


connection_string = """

Server=10.10.241.79,1433;
Initial Catalog=Demo;
User ID=sa;
Password=123456;

"""


print()
print("=" * 60)
print("KEYWORD DISCOVERY")
print("=" * 60)
print()

print(
    contains_connection_string(
        connection_string
    )
)

print()