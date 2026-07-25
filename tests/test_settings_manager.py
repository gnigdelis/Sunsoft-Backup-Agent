from pprint import pprint

from core.settings_manager import (
    SettingsManager,
)


manager = SettingsManager()


print()
print("CREATING SETTINGS FILE")
print()

result = manager.create_default_settings()

pprint(result)


print()
print("READING SETTINGS FILE")
print()

result = manager.read_settings()

pprint(result)


print()
print("DESTINATION PATH")
print()

print(
    result["data"]["destination_path"]
)


print()
print("DELETE TEMP FILES")
print()

print(
    result["data"]["delete_temp_files"]
)