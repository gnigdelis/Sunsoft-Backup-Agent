from pprint import pprint

from core.health.health_check_manager import (
    HealthCheckManager,
)


health = HealthCheckManager()


health.add_warning(

    "ProgramData folder is empty."

)

health.add_error(

    "SQL Server service is stopped."

)

health.add_recommendation(

    "Start SQL Server service."

)

health.add_recommendation(

    "Verify ProgramData files."

)


result = health.get_result()


pprint(
    result
)