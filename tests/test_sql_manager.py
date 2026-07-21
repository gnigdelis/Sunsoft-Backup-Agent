from pprint import pprint

from core.managers.sql_manager import (
    SQLManager,
)


sql_manager = SQLManager()

result = (

    sql_manager
    .get_sql_information()

)

pprint(
    result
)