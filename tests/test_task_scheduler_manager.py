from pprint import pprint

from core.managers.task_scheduler_manager import (
    TaskSchedulerManager,
)


manager = TaskSchedulerManager()

result = manager.get_information()

pprint(
    result
)