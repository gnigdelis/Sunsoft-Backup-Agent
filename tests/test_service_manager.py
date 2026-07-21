from pprint import pprint

from core.windows.service_manager import (
    WindowsServiceManager,
)


service_manager = WindowsServiceManager()


#
# SQL SERVER TEST
#

result = service_manager.get_service_information(
    "MSSQLSERVER"
)


pprint(
    result
)