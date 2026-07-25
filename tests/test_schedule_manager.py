from pprint import pprint

from core.schedule_manager import (
    ScheduleManager,
)


manager = ScheduleManager()

result = manager.create_daily_schedule(
    time="03:00",
    executable_path=r"C:\Windows\System32\notepad.exe",
)

print(type(result))
print()
pprint(result)