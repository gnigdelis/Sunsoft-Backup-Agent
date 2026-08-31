from pathlib import Path

from PySide6.QtGui import QTextDocument
from PySide6.QtPrintSupport import QPrinter


class MyDataPDF:

    @staticmethod
    def save_invoice(
        invoice,
        parent=None,
    ):

        from PySide6.QtWidgets import QFileDialog

        default_name = (
            f"MyData_{invoice.aa}_"
            f"{invoice.issue_date}.pdf"
        )

        file_path, _ = QFileDialog.getSaveFileName(
            parent,
            "Αποθήκευση παραστατικού PDF",
            default_name,
            "PDF Files (*.pdf)",
        )

        if not file_path:
            return False

        output_path = Path(file_path)

        document = QTextDocument()

        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: Arial;
                    font-size: 11pt;
                }}

                h1 {{
                    font-size: 18pt;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}

                td {{
                    border: 1px solid #cccccc;
                    padding: 8px;
                }}

                .label {{
                    font-weight: bold;
                    width: 30%;
                }}
            </style>
        </head>

        <body>

            <h1>MyData Sent</h1>

            <table>

                <tr>
                    <td class="label">Type</td>
                    <td>{invoice.invoice_type}</td>
                </tr>

                <tr>
                    <td class="label">Document</td>
                    <td>{invoice.document_name}</td>
                </tr>

                <tr>
                    <td class="label">Date</td>
                    <td>{invoice.issue_date}</td>
                </tr>

                <tr>
                    <td class="label">A/A</td>
                    <td>{invoice.aa}</td>
                </tr>

                <tr>
                    <td class="label">VAT No.</td>
                    <td>{invoice.cust_afm}</td>
                </tr>

                <tr>
                    <td class="label">Invoice ID</td>
                    <td>{invoice.invoice_id}</td>
                </tr>

                <tr>
                    <td class="label">Status</td>
                    <td>Sent</td>
                </tr>

            </table>

        </body>
        </html>
        """

        document.setHtml(
            html
        )

        printer = QPrinter(
            QPrinter.PrinterMode.HighResolution
        )

        printer.setOutputFormat(
            QPrinter.OutputFormat.PdfFormat
        )

        printer.setOutputFileName(
            str(output_path)
        )

        document.print_(
            printer
        )

        if not output_path.exists():
            raise RuntimeError(
                "Το PDF δεν δημιουργήθηκε."
            )

        if output_path.stat().st_size <= 0:
            raise RuntimeError(
                "Το PDF δημιουργήθηκε αλλά είναι κενό."
            )

        return True
