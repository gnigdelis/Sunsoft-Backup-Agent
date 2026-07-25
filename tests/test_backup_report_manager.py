from pprint import pprint

from core.backup_report_manager import (
    BackupReportManager,
)


manager = BackupReportManager()

report_lines = [

    "SUNSOFT BACKUP REPORT",
    "",
    "========================================",
    "",
    "SQL BACKUP ........ SUCCESS",
    "PRINTER BACKUP .... SUCCESS",
    "ZIP FILE .......... SUCCESS",
    "DESTINATION ....... SUCCESS",
    "",
    "FINAL STATUS ...... SUCCESS",
]

result = manager.create_report(
    session_path="temp",
    report_lines=report_lines,
)

print(type(result))
print()

pprint(result)