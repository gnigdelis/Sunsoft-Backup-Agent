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


files_to_inspect = (

    results["critical_files"]

    +

    results["important_files"]

)


print()
print("=" * 80)
print("SUNSOFT BACKUP AGENT - CONFIGURATION INSPECTOR")
print("=" * 80)
print()


for file in files_to_inspect:

    print("=" * 80)
    print()

    print(
        f"MODULE : {file['module_name']}"
    )

    print(
        f"FILE   : {file['file_name']}"
    )

    print()

    raw_result = read_raw_file(
        file["full_path"]
    )

    if not raw_result["success"]:

        print("FAILED TO READ FILE")
        print()

        continue

    print("-" * 80)
    print()

    print("FIRST 30 LINES")
    print()

    lines = (
        raw_result["content"]
        .splitlines()
    )

    for line in lines[:30]:

        print(line)

    print()