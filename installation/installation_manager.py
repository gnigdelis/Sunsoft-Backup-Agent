from pathlib import Path
from typing import List

from core.module_snapshot import ModuleSnapshot


PROGRAM_FILES_PATH = Path(
    r"C:\Program Files (x86)\Sunsoft Ltd"
)

PROGRAM_DATA_PATH = Path(
    r"C:\ProgramData\Sunsoft"
)


def installation_exists() -> bool:

    return (
        PROGRAM_FILES_PATH.exists()
        or
        PROGRAM_DATA_PATH.exists()
    )


def discover_installation_paths() -> List[str]:

    paths = []

    if PROGRAM_FILES_PATH.exists():
        paths.append(str(PROGRAM_FILES_PATH))

    if PROGRAM_DATA_PATH.exists():
        paths.append(str(PROGRAM_DATA_PATH))

    return paths


def discover_modules() -> List[ModuleSnapshot]:

    modules = {}

    #
    # PROGRAM FILES
    #

    if PROGRAM_FILES_PATH.exists():

        for item in PROGRAM_FILES_PATH.iterdir():

            if not item.is_dir():
                continue

            module_name = item.name

            modules[module_name] = ModuleSnapshot(
                module_name=module_name,
                program_files_path=str(item),
                has_program_files=True
            )

    #
    # PROGRAM DATA
    #

    if PROGRAM_DATA_PATH.exists():

        for item in PROGRAM_DATA_PATH.iterdir():

            if not item.is_dir():
                continue

            module_name = item.name

            if module_name in modules:

                modules[module_name].program_data_path = (
                    str(item)
                )

                modules[module_name].has_program_data = True

            else:

                modules[module_name] = ModuleSnapshot(
                    module_name=module_name,
                    program_data_path=str(item),
                    has_program_data=True
                )

    return list(modules.values())


def discover_installation():

    return {

        "installation_found":
        installation_exists(),

        "installation_paths":
        discover_installation_paths(),

        "installed_modules":
        discover_modules(),

    }


if __name__ == "__main__":

    result = discover_installation()

    print()
    print("=" * 60)
    print("SUNSOFT BACKUP AGENT - INSTALLATION DISCOVERY")
    print("=" * 60)
    print()

    print(
        f"Installation Found : "
        f"{result['installation_found']}"
    )

    print()

    print("Installation Paths")
    print("-" * 60)

    for path in result["installation_paths"]:

        print(path)

    print()

    print("Installed Modules")
    print("-" * 60)

    for module in result["installed_modules"]:

        print()

        print(f"Module Name : {module.module_name}")
        print(
            f"Program Files : "
            f"{module.has_program_files}"
        )
        print(
            f"Program Data : "
            f"{module.has_program_data}"
        )

    print()