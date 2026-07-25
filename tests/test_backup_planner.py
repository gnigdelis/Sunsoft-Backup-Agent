from pprint import pprint

from core.planner.backup_planner import (
    BackupPlanner,
)


planner = BackupPlanner()


planner.include_target(
    "sql"
)

planner.include_target(
    "programdata"
)

planner.include_target(
    "printers"
)

planner.skip_target(

    "network",

    warning=(
        "Network target skipped."
    ),

)

planner.add_recommendation(

    "Verify network configuration."

)

result = planner.get_result()


pprint(
    result
)