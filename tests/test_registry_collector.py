from core.managers.registry_manager import (
    RegistryManager,
)

from core.collectors.registry_collector import (
    RegistryCollector,
)


manager = RegistryManager()

collector = RegistryCollector()


result = manager.get_information()


collector.export_json(

    result,
    "backup_test/registry",

)

print(

    "Registry export completed successfully."

)