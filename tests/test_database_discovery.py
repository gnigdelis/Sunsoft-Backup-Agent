from pprint import pprint

from core.discovery.database_discovery import (
    DatabaseDiscovery,
)


database = DatabaseDiscovery()

result = database.discover()

pprint(
    result
)