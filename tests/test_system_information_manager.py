from pprint import pprint

from core.system_information_manager import (
    SystemInformationManager,
)

manager = SystemInformationManager()

result = (
    manager.get_system_information()
)

print(type(result))
print()

pprint(result)