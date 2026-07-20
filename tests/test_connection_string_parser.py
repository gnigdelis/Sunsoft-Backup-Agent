from intelligence.connection_string_parser import (
    parse_connection_string,
)


connection_string = """
Server=10.10.241.79,1433;
Initial Catalog=ExternalConnectionWebApi;
User ID=sa;
Password=123456;
"""


result = parse_connection_string(
    connection_string
)


print()
print("=" * 60)
print("CONNECTION STRING PARSER")
print("=" * 60)
print()

for key, value in result.items():

    print(
        f"{key} : {value}"
    )

print()