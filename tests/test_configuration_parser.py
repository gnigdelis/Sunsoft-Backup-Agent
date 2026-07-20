from configuration.configuration_manager import (
    discover_configuration_files,
)

from configuration.configuration_filter import (
    filter_configuration_files,
)

from configuration.configuration_parser import (
    parse_configuration_files,
)


configuration_files = discover_configuration_files()

results = filter_configuration_files(
    configuration_files
)

files_to_parse = (
    results["critical_files"]
    +
    results["important_files"]
)

parsed_results = parse_configuration_files(
    files_to_parse
)

print()
print("=" * 60)
print("CONFIGURATION PARSER ENGINE")
print("=" * 60)
print()

print(
    f"Files Parsed : "
    f"{len(parsed_results)}"
)

print()

for result in parsed_results:

    print("-" * 60)

    print(f"Module : {result.module_name}")
    print(f"File : {result.file_name}")
    print(f"Status : {result.parse_status}")

print()