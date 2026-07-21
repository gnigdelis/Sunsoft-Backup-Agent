import win32print


class PrinterManager:

    def __init__(self):

        pass

    def get_printers(self):

        printers = []

        try:

            flags = (
                win32print.PRINTER_ENUM_LOCAL |
                win32print.PRINTER_ENUM_CONNECTIONS
            )

            installed_printers = (

                win32print.EnumPrinters(
                    flags
                )

            )

            default_printer = (

                win32print.GetDefaultPrinter()

            )

            for printer in installed_printers:

                printer_name = printer[2]

                printers.append(

                    {

                        "name":
                            printer_name,

                        "default_printer":
                            printer_name ==
                            default_printer,

                    }

                )

        except Exception:

            pass

        return printers

    def get_information(self):

        printers = self.get_printers()

        warnings = []

        status = "SUCCESS"

        if len(printers) == 0:

            status = "WARNING"

            warnings.append(

                "No printers found."

            )

        return {

            "success": True,

            "status": status,

            "warnings": warnings,

            "errors": [],

            "data": printers,

        }