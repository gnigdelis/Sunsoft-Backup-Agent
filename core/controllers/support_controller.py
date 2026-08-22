from PySide6.QtCore import QObject, Signal

from core.support.support_service import SupportService


class SupportController(QObject):

    search_completed = Signal(object)

    search_failed = Signal(str)

    reset_completed = Signal(object)

    reset_failed = Signal(str)

    def __init__(self, udl_path: str):

        super().__init__()

        self.service = SupportService(
            udl_path
        )

    def search_invoice(

        self,

        invoice_number: int,

        invoice_date: str,

    ):

        try:

            result = self.service.search_invoice(

                invoice_number,

                invoice_date,

            )

            if result.found:

                self.search_completed.emit(
                    result
                )

            else:

                self.search_failed.emit(
                    result.message
                )

        except Exception as ex:

            self.search_failed.emit(
                str(ex)
            )

    def reset_status(

        self,

        oid: int,

    ):

        try:

            result = self.service.reset_status(
                oid
            )

            self.reset_completed.emit(
                result
            )

        except Exception as ex:

            self.reset_failed.emit(
                str(ex)
            )