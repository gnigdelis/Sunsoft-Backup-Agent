from pprint import pprint

from core.discovery.system_discovery import (
    SystemDiscovery,
)


system = SystemDiscovery()

result = system.discover()


pprint(
    result
)