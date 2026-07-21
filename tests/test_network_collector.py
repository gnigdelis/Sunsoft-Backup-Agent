from core.managers.network_manager import (
    NetworkManager,
)

from core.collectors.network_collector import (
    NetworkCollector,
)


manager = NetworkManager()

collector = NetworkCollector()


result = manager.get_information()


collector.export_json(

    result,
    "backup_test/network",

)

print(

    "Network export completed successfully."

)