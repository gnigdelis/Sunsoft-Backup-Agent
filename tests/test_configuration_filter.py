from configuration.configuration_manager import (
    discover_configuration_files,
)

from configuration.configuration_filter import (
    filter_configuration_files,
)


configuration_files = discover_configuration_files()

results = filter_configuration_files(
    configuration_files
)


print()
print("=" * 60)
print("CONFIGURATION FILTER ENGINE")
print("=" * 60)
print()

print(
    f"Critical Files : "
    f"{len(results['critical_files'])}"
)

print(
    f"Important Files : "
    f"{len(results['important_files'])}"
)

print(
    f"Ignored Files : "
    f"{len(results['ignored_files'])}"
)

print(
    f"Unknown Files : "
    f"{len(results['unknown_files'])}"
)

print()

print("CRITICAL FILES")
print("-" * 60)

for file in results["critical_files"]:

    print(file["file_name"])

print()

print("IMPORTANT FILES")
print("-" * 60)

for file in results["important_files"]:

    print(file["file_name"])

print()

print("UNKNOWN FILES")
print("-" * 60)

for file in results["unknown_files"]:

    print(file["file_name"])

print()