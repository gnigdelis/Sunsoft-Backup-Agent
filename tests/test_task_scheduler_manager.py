from pprint import pprint

from core.scheduler.task_scheduler_manager import (
    TaskSchedulerManager,
)

manager = TaskSchedulerManager()

print("\nTASK EXISTS (BEFORE)\n")

pprint(
    manager.task_exists()
)

print("\nCREATE POLICY TASK\n")

pprint(
    manager.create_policy_task()
)

print("\nTASK EXISTS (AFTER CREATE)\n")

pprint(
    manager.task_exists()
)

print("\nDELETE POLICY TASK\n")

pprint(
    manager.delete_policy_task()
)

print("\nTASK EXISTS (AFTER DELETE)\n")

pprint(
    manager.task_exists()
)