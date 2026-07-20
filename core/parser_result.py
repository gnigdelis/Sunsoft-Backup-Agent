from dataclasses import dataclass
from typing import Any


@dataclass
class ParserResult:

    module_name: str = ""

    file_name: str = ""

    full_path: str = ""

    parse_success: bool = False

    parse_status: str = ""

    parsed_data: Any = None