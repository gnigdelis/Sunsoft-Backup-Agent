from pprint import pprint

from core.compression.compression_engine import (
    CompressionEngine,
)


engine = CompressionEngine()


result = (
    engine.create_backup_zip()
)


pprint(result)