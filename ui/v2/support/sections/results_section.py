from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.cards.base_card import BaseCard


class ResultsSection(BaseCard):

    delete_clicked = Signal()

    def __init__(self):

        super().__init__(
            title="Pending Order",
            minimum_height=340,
        )

        self.order_number = None
        self.order_date = None
        self.rows = []

        self.setup_content()

    # ==========================================================
    # UI
    # ==========================================================

    def setup_content(self):

        self.content_layout.setSpacing(
            12
        )

        # ======================================================
        # ACCENT
        # ======================================================

        accent = QLabel()

        accent.setFixedHeight(
            3
        )

        accent.setStyleSheet(
            """
            QLabel {
                background:#FF9800;
                border:none;
            }
            """
        )

        self.content_layout.insertWidget(
            0,
            accent
        )

        # ======================================================
        # DESCRIPTION
        # ======================================================

        self.description = QLabel(
            "No pending order selected."
        )

        self.description.setWordWrap(
            True
        )

        self.description.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        self.content_layout.addWidget(
            self.description
        )

        # ======================================================
        # SUMMARY
        # ======================================================

        self.summary = QLabel(
            "Waiting for search..."
        )

        self.summary.setWordWrap(
            True
        )

        self.summary.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:10pt;
                font-weight:700;
            }}
            """
        )

        self.content_layout.addWidget(
            self.summary
        )

        # ======================================================
        # RECORDS
        # ======================================================

        self.records = QLabel()

        self.records.setWordWrap(
            True
        )

        self.records.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.records.setStyleSheet(
            """
            QLabel {
                color:#D5D7DC;
                background:#202226;
                border:1px solid #35383F;
                padding:10px;
                font-size:9pt;
            }
            """
        )

        self.content_layout.addWidget(
            self.records
        )

        # ======================================================
        # DELETE BUTTON
        # ======================================================

        self.delete_button = QPushButton(
            "■  Delete Pending Order"
        )

        self.delete_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.delete_button.setMinimumHeight(
            40
        )

        self.delete_button.setEnabled(
            False
        )

        self.delete_button.setStyleSheet(
            """
            QPushButton {
                background:transparent;
                color:#E53935;
                border:none;
                padding:0;
                font-size:10pt;
                font-weight:700;
                text-align:left;
            }

            QPushButton:hover {
                color:#FF4B4B;
            }

            QPushButton:pressed {
                color:#C62828;
            }

            QPushButton:disabled {
                color:#666A71;
            }
            """
        )

        self.delete_button.clicked.connect(
            self._emit_delete
        )

        self.content_layout.addWidget(
            self.delete_button
        )

        # ======================================================
        # STATUS
        # ======================================================

        self.result_status = QLabel(
            "Waiting for search..."
        )

        self.result_status.setWordWrap(
            True
        )

        self.result_status.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        self.content_layout.addWidget(
            self.result_status
        )

        self.content_layout.addStretch()

    # ==========================================================
    # SHOW RESULT
    # ==========================================================

    def show_result(
        self,
        order_number,
        order_date,
        rows,
        pending_records,
        total_records,
    ):

        self.order_number = order_number
        self.order_date = order_date

        self.rows = list(
            rows
            if rows
            else []
        )

        self.description.setText(
            "Order found."
        )

        self.summary.setText(
            (
                f"Order {order_number}  •  "
                f"Date {order_date}  •  "
                f"{pending_records} pending / "
                f"{total_records} total"
            )
        )

        lines = []

        for index, row in enumerate(
            self.rows,
            start=1
        ):

            oid = row.get(
                "SalesTransOID",
                "-"
            )

            status = row.get(
                "SalesTransStatus",
                "-"
            )

            note_code = row.get(
                "SalesTransNoteCode",
                "-"
            )

            status_text = (
                "CLOSED"
                if status == 1
                else "PENDING"
            )

            lines.append(
                (
                    f"{index}.  "
                    f"OID: {oid}   |   "
                    f"Status: {status}   |   "
                    f"{status_text}   |   "
                    f"Code: {note_code}"
                )
            )

        if lines:

            self.records.setText(
                "\n".join(
                    lines
                )
            )

        else:

            self.records.setText(
                "No records returned."
            )

        if pending_records > 0:

            self.delete_button.setEnabled(
                True
            )

            self.result_status.setText(
                (
                    f"{pending_records} "
                    "record(s) need to be closed."
                )
            )

            self.result_status.setStyleSheet(
                """
                QLabel {
                    color:#FF9800;
                    font-size:9pt;
                    font-weight:600;
                }
                """
            )

        else:

            self.delete_button.setEnabled(
                False
            )

            self.result_status.setText(
                "Order is already closed."
            )

            self.result_status.setStyleSheet(
                """
                QLabel {
                    color:#53C653;
                    font-size:9pt;
                    font-weight:600;
                }
                """
            )

    # ==========================================================
    # NOT FOUND
    # ==========================================================

    def show_not_found(
        self
    ):

        self.clear_result()

        self.description.setText(
            "No order was found for the supplied number and date."
        )

        self.result_status.setText(
            "Order not found."
        )

        self.result_status.setStyleSheet(
            """
            QLabel {
                color:#FF9800;
                font-size:9pt;
                font-weight:600;
            }
            """
        )

    # ==========================================================
    # ERROR
    # ==========================================================

    def show_error(
        self,
        message
    ):

        self.clear_result()

        self.description.setText(
            "The search could not be completed."
        )

        self.result_status.setText(
            str(
                message
            )
        )

        self.result_status.setStyleSheet(
            """
            QLabel {
                color:#FF5C5C;
                font-size:9pt;
                font-weight:600;
            }
            """
        )

    # ==========================================================
    # DELETE SIGNAL
    # ==========================================================

    def _emit_delete(
        self
    ):

        self.delete_clicked.emit()

    # ==========================================================
    # DELETE SUCCESS
    # ==========================================================

    def show_deleted(
        self,
        affected_rows
    ):

        self.delete_button.setEnabled(
            False
        )

        self.result_status.setText(
            (
                f"Successfully closed "
                f"{affected_rows} pending record(s)."
            )
        )

        self.result_status.setStyleSheet(
            """
            QLabel {
                color:#53C653;
                font-size:9pt;
                font-weight:600;
            }
            """
        )

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear_result(
        self
    ):

        self.order_number = None
        self.order_date = None
        self.rows = []

        self.description.setText(
            "No pending order selected."
        )

        self.summary.setText(
            "Waiting for search..."
        )

        self.records.clear()

        self.result_status.setText(
            "Waiting for search..."
        )

        self.result_status.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        self.delete_button.setEnabled(
            False
        )