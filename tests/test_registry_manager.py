from pprint import pprint

from core.managers.registry_manager import (
    RegistryManager,
)


manager = RegistryManager()

result = manager.get_information()

pprint(
    result
)