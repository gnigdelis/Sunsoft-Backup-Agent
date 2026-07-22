from core.managers.applications_manager import (
    ApplicationsManager,
)

from core.collectors.applications_collector import (
    ApplicationsCollector,
)


manager = ApplicationsManager()

collector = ApplicationsCollector()


result = manager.get_information()

collector.export_json(

    result,
    "backup_test/applications",

)

print(

    "Applications export completed successfully."

)