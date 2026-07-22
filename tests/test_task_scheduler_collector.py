from core.managers.task_scheduler_manager import (
    TaskSchedulerManager,
)

from core.collectors.task_scheduler_collector import (
    TaskSchedulerCollector,
)


manager = TaskSchedulerManager()

collector = TaskSchedulerCollector()


result = manager.get_information()


collector.export_json(

    result,
    "backup_test/taskscheduler",

)


print(

    "Scheduled Tasks export completed successfully."

)