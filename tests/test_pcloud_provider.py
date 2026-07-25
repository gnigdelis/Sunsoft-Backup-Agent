from pprint import pprint

from core.providers.pcloud_provider import (
    PCloudProvider,
)


provider = PCloudProvider()


result = provider.validate_path(

    r"P:\Sunsoft Guardian\Backups"

)


pprint(
    result
)