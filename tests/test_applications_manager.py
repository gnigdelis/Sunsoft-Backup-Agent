from pprint import pprint

from core.managers.applications_manager import (
    ApplicationsManager,
)


manager = ApplicationsManager()

result = manager.get_information()

pprint(
    result
)