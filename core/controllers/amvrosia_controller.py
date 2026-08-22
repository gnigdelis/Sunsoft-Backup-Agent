from PySide6.QtCore import QObject, Signal

from core.services.amvrosia_service import (
    amvrosia_service,
)


class AmvrosiaController(QObject):

    search_completed = Signal(object)

    repair_completed = Signal(object)

    failed = Signal(str)

    def __init__(self):

        super().__init__()

    def search_order(
        self,
        order_number: int,
    ):

        try:

            result = amvrosia_service.search_order(
                order_number
            )

            self.search_completed.emit(
                result
            )

        except Exception as ex:

            self.failed.emit(
                str(ex)
            )

    def repair_order(
        self,
        order_number: int,
    ):

        try:

            result = amvrosia_service.repair_order(
                order_number
            )

            self.repair_completed.emit(
                result
            )

        except Exception as ex:

            self.failed.emit(
                str(ex)
            )