from pprint import pprint

from core.managers.printer_manager import (
    PrinterManager,
)


manager = PrinterManager()

result = manager.get_information()

pprint(
    result
)