from dataclasses import dataclass


@dataclass
class ModuleSnapshot:

    module_name: str = ""

    program_files_path: str = ""

    program_data_path: str = ""

    has_program_files: bool = False

    has_program_data: bool = False