from pprint import pprint

from core.cleanup_manager import (
    CleanupManager,
)


manager = CleanupManager()

print()
print("DELETE DIRECTORY")
print()

result = manager.delete_directory(
    directory_path="zip_test",
)

pprint(result)

print()
print("DELETE FILE")
print()

result = manager.delete_file(
    file_path="settings.ini",
)

pprint(result)