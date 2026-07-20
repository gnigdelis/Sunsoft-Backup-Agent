from pathlib import Path


SUNSOFT_ROOT = Path(r"C:\Program Files (x86)\Sunsoft Ltd")


SUPPORTED_EXTENSIONS = [
    ".json",
    ".config",
    ".xml"
]


def discover_configuration_files():

    configuration_files = []

    if not SUNSOFT_ROOT.exists():
        return configuration_files

    for module in SUNSOFT_ROOT.iterdir():

        if not module.is_dir():
            continue

        for file in module.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix.lower() in SUPPORTED_EXTENSIONS:

                configuration_files.append(
                    {
                        "module_name": module.name,
                        "file_name": file.name,
                        "full_path": str(file),
                        "extension": file.suffix
                    }
                )

    return configuration_files


if __name__ == "__main__":

    files = discover_configuration_files()

    print()
    print("=" * 60)
    print("SUNSOFT BACKUP AGENT - CONFIGURATION DISCOVERY")
    print("=" * 60)
    print()

    for file in files:

        print(f"MODULE      : {file['module_name']}")
        print(f"FILE        : {file['file_name']}")
        print(f"EXTENSION   : {file['extension']}")
        print(f"PATH        : {file['full_path']}")
        print("-" * 60)