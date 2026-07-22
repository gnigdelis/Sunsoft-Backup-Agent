from pprint import pprint

from core.managers.sunsoft_services_manager import (
    SunsoftServicesManager,
)


manager = SunsoftServicesManager()

result = manager.get_information()

pprint(
    result
)