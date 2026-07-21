from pprint import pprint

from core.managers.network_manager import (
    NetworkManager,
)


manager = NetworkManager()

result = manager.get_information()

pprint(
    result
)