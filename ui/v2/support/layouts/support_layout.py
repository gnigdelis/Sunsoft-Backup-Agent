from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
)

from core.services.support_service import SupportService
from core.database.database_context import database_context

from ui.v2.styles.theme import Theme

from ui.v2.support.sections.search_section import SearchSection
from ui.v2.support.sections.results_section import ResultsSection


class SupportLayout(QWidget):

    def __init__(self):

        super().__init__()

        self.service = SupportService()

        self.setup_ui()

        self.connect_events()

        database_context.database_changed.connect(
            self.update_connection_status
        )

        self.update_connection_status(
            database_context.active()
        )

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            20,
            18,
            20,
            22
        )

        root.setSpacing(
            14
        )

        # ======================================================
        # HEADER
        # ======================================================

        header = QHBoxLayout()

        title_block = QVBoxLayout()

        title_block.setSpacing(
            2
        )

        title = QLabel(
            "Delete Pending Order"
        )

        title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:24pt;
                font-weight:700;
            }
            """
        )

        subtitle = QLabel(
            "Find and close pending records of an order"
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:10pt;
            }
            """
        )

        title_block.addWidget(
            title
        )

        title_block.addWidget(
            subtitle
        )

        header.addLayout(
            title_block
        )

        header.addStretch()

        self.connection_status = QLabel(
            "Not Connected"
        )

        self.connection_status.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        header.addWidget(
            self.connection_status
        )

        root.addLayout(
            header
        )

        # ======================================================
        # CONTENT
        # ======================================================

        content = QHBoxLayout()

        content.setContentsMargins(
            0,
            0,
            0,
            0
        )

        content.setSpacing(
            16
        )

        self.search_section = SearchSection()

        self.results_section = ResultsSection()

        content.addWidget(
            self.search_section,
            1
        )

        content.addWidget(
            self.results_section,
            1
        )

        root.addLayout(
            content,
            1
        )

        # ======================================================
        # FOOTER STATUS
        # ======================================================

        self.page_status = QLabel(
            "Ready."
        )

        self.page_status.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                background:#202226;
                border:1px solid #34373D;
                padding:7px 10px;
                font-size:8.5pt;
            }}
            """
        )

        root.addWidget(
            self.page_status
        )

    # ==========================================================
    # EVENTS
    # ==========================================================

    def connect_events(self):

        self.search_section.search_clicked.connect(
            self._search_order
        )

        self.results_section.delete_clicked.connect(
            self._delete_pending_order
        )

    # ==========================================================
    # CONNECTION STATUS
    # ==========================================================

    def update_connection_status(
        self,
        database
    ):

        if database:

            self.connection_status.setText(
                "Connected"
            )

            self.connection_status.setStyleSheet(
                """
                QLabel {
                    color:#53C653;
                    background:transparent;
                    border:none;
                    padding:0;
                    font-size:9pt;
                    font-weight:700;
                }
                """
            )

        else:

            self.connection_status.setText(
                "Not Connected"
            )

            self.connection_status.setStyleSheet(
                """
                QLabel {
                    color:#FF9800;
                    background:transparent;
                    border:none;
                    padding:0;
                    font-size:9pt;
                    font-weight:700;
                }
                """
            )

    # ==========================================================
    # SEARCH
    # ==========================================================

    def _search_order(
        self,
        order_number,
        order_date,
    ):

        if not database_context.active():

            QMessageBox.warning(
                self,
                "Database Required",
                "Please select a database from the Dashboard.",
            )

            return

        self.results_section.clear_result()

        self.search_section.set_busy(
            True
        )

        self.page_status.setText(
            "Searching order..."
        )

        try:

            result = (
                self.service.search_invoice(
                    order_number,
                    order_date,
                )
            )

            if not result.found:

                self.results_section.show_not_found()

                self.search_section.set_status(
                    result.message
                    or "Order not found.",
                    "warning"
                )

                self.page_status.setText(
                    "Order not found."
                )

                return

            self.results_section.show_result(
                order_number=order_number,
                order_date=order_date,
                rows=result.rows,
                pending_records=result.pending_records,
                total_records=result.total_records,
            )

            if result.pending_records > 0:

                self.search_section.set_status(
                    (
                        f"Order found. "
                        f"{result.pending_records} "
                        "pending record(s)."
                    ),
                    "warning"
                )

                self.page_status.setText(
                    "Pending records found. Ready to close."
                )

            else:

                self.search_section.set_status(
                    "Order is already closed.",
                    "success"
                )

                self.page_status.setText(
                    "No pending records found."
                )

        except Exception as error:

            self.results_section.show_error(
                str(error)
            )

            self.search_section.set_status(
                str(error),
                "error"
            )

            self.page_status.setText(
                "Search failed."
            )

        finally:

            self.search_section.set_busy(
                False
            )

    # ==========================================================
    # CLOSE PENDING ORDER
    # ==========================================================

    def _delete_pending_order(
        self
    ):

        order_number = (
            self.results_section.order_number
        )

        order_date = (
            self.results_section.order_date
        )

        if (
            order_number is None
            or order_date is None
        ):

            return

        confirmation = QMessageBox(
            self
        )

        confirmation.setWindowTitle(
            "Delete Pending Order"
        )

        confirmation.setText(
            (
                f"Close the pending records "
                f"of order {order_number}?"
            )
        )

        confirmation.setInformativeText(
            (
                "All records of this order whose "
                "SalesTransStatus is different from 1 "
                "will be changed to 1."
            )
        )

        delete_button = (
            confirmation.addButton(
                "Delete",
                QMessageBox.AcceptRole
            )
        )

        confirmation.addButton(
            "Cancel",
            QMessageBox.RejectRole
        )

        confirmation.exec()

        if (
            confirmation.clickedButton()
            != delete_button
        ):

            return

        self.results_section.delete_button.setEnabled(
            False
        )

        self.page_status.setText(
            "Closing pending order..."
        )

        try:

            result = (
                self.service.close_pending_order(
                    order_number,
                    order_date,
                )
            )

            if not result.get(
                "success",
                False
            ):

                message = (
                    result.get(
                        "message",
                        "Unable to close pending order."
                    )
                )

                self.results_section.result_status.setText(
                    message
                )

                self.results_section.result_status.setStyleSheet(
                    """
                    QLabel {
                        color:#FF5C5C;
                        font-size:9pt;
                        font-weight:600;
                    }
                    """
                )

                self.page_status.setText(
                    "Operation failed."
                )

                return

            affected_rows = (
                result.get(
                    "affected_rows",
                    0
                )
            )

            self.results_section.show_deleted(
                affected_rows
            )

            self.search_section.set_status(
                (
                    f"Closed {affected_rows} "
                    "pending record(s)."
                ),
                "success"
            )

            self.page_status.setText(
                (
                    f"Order {order_number} "
                    "closed successfully."
                )
            )

        except Exception as error:

            self.results_section.result_status.setText(
                str(error)
            )

            self.results_section.result_status.setStyleSheet(
                """
                QLabel {
                    color:#FF5C5C;
                    font-size:9pt;
                    font-weight:600;
                }
                """
            )

            self.page_status.setText(
                "Operation failed."
            )