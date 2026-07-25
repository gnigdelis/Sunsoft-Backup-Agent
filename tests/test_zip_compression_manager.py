from pprint import pprint

from core.zip_compression_manager import (
    ZipCompressionManager,
)

manager = ZipCompressionManager()

result = manager.create_zip(
    source_directory="zip_test",
    output_directory="zip_output",
)

print(type(result))
print()

pprint(result)