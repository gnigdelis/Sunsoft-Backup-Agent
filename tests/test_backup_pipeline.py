from pprint import pprint

from core.backup_pipeline import (
    BackupPipeline,
)


pipeline = BackupPipeline()

result = (
    pipeline.execute()
)

pprint(result)