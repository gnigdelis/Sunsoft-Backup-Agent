from configuration.configuration_manager import (
    discover_configuration_files,
)

from configuration.configuration_filter import (
    filter_configuration_files,
)

from configuration.configuration_raw_reader import (
    read_raw_file,
)


configuration_files = discover_configuration_files()

results = filter_configuration_files(
    configuration_files
)

files_to_read = (
    results["critical_files"]
    +
    results["important_files"]
)


print()
print("=" * 60)
print("CONFIGURATION RAW READER")
print("=" * 60)
print()


for file in files_to_read:

    result = read_raw_file(
        file["full_path"]
    )

    print("-" * 60)

    print(
        f"Module : "
        f"{file['module_name']}"
    )

    print(
        f"File : "
        f"{file['file_name']}"
    )

    print(
        f"Success : "
        f"{result['success']}"
    )

    print(
        f"Encoding : "
        f"{result['encoding']}"
    )

print()