from pprint import pprint

from core.managers.programdata_manager import (
    ProgramDataManager,
)


manager = ProgramDataManager()

result = manager.get_information()

pprint(
    result
)