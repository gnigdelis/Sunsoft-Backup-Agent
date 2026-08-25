from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QDateEdit,
    QGridLayout,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.cards.base_card import BaseCard


class SearchSection(BaseCard):

    search_clicked = Signal(int, str)

    def __init__(self):

        super().__init__(
            title="Search Pending Order",
            minimum_height=300,
        )

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
                background:#00ACC1;
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

        description = QLabel(
            "Enter the order number and date to find pending records."
        )

        description.setWordWrap(
            True
        )

        description.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        self.content_layout.addWidget(
            description
        )

        # ======================================================
        # ORDER NUMBER
        # ======================================================

        order_label = QLabel(
            "Order Number"
        )

        order_label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
                font-weight:600;
            }}
            """
        )

        self.invoice = QLineEdit()

        self.invoice.setPlaceholderText(
            "Enter order number"
        )

        self.invoice.setClearButtonEnabled(
            True
        )

        input_style = f"""
            QLineEdit,
            QDateEdit {{
                background:#202226;
                color:{Theme.Colors.TEXT};
                border:1px solid #3A3D43;
                padding:8px 10px;
                min-height:36px;
                border-radius:0px;
                selection-background-color:#00ACC1;
            }}

            QLineEdit:focus,
            QDateEdit:focus {{
                border:1px solid #00ACC1;
            }}
        """

        self.invoice.setStyleSheet(
            input_style
        )

        # ======================================================
        # ORDER DATE
        # ======================================================

        date_label = QLabel(
            "Order Date"
        )

        date_label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
                font-weight:600;
            }}
            """
        )

        self.date = QDateEdit()

        self.date.setCalendarPopup(
            True
        )

        self.date.setDate(
            QDate.currentDate()
        )

        self.date.setDisplayFormat(
            "dd/MM/yyyy"
        )

        self.date.setStyleSheet(
            input_style
        )

        # ======================================================
        # FORM
        # ======================================================

        form = QGridLayout()

        form.setContentsMargins(
            0,
            4,
            0,
            0
        )

        form.setHorizontalSpacing(
            16
        )

        form.setVerticalSpacing(
            10
        )

        form.addWidget(
            order_label,
            0,
            0
        )

        form.addWidget(
            self.invoice,
            0,
            1
        )

        form.addWidget(
            date_label,
            1,
            0
        )

        form.addWidget(
            self.date,
            1,
            1
        )

        form.setColumnStretch(
            1,
            1
        )

        self.content_layout.addLayout(
            form
        )

        # ======================================================
        # SEARCH BUTTON
        # ======================================================

        self.search_button = QPushButton(
            "▶  Search Order"
        )

        self.search_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.search_button.setMinimumHeight(
            40
        )

        self.search_button.setStyleSheet(
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

        self.search_button.clicked.connect(
            self._emit_search
        )

        self.invoice.returnPressed.connect(
            self._emit_search
        )

        self.content_layout.addWidget(
            self.search_button
        )

        # ======================================================
        # STATUS
        # ======================================================

        self.status_label = QLabel(
            "Waiting for order..."
        )

        self.status_label.setWordWrap(
            True
        )

        self.status_label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        self.content_layout.addWidget(
            self.status_label
        )

        self.content_layout.addStretch()

    # ==========================================================
    # SEARCH
    # ==========================================================

    def _emit_search(self):

        value = self.invoice.text().strip()

        if not value:

            self.set_status(
                "Enter an order number.",
                "warning"
            )

            return

        try:

            order_number = int(
                value
            )

        except ValueError:

            self.set_status(
                "Order number must be numeric.",
                "error"
            )

            return

        order_date = (
            self.date.date().toString(
                "yyyyMMdd"
            )
        )

        self.search_clicked.emit(
            order_number,
            order_date,
        )

    # ==========================================================
    # STATUS
    # ==========================================================

    def set_status(
        self,
        message,
        state="normal"
    ):

        if state == "success":

            color = "#53C653"

        elif state == "warning":

            color = "#FF9800"

        elif state == "error":

            color = "#FF5C5C"

        else:

            color = Theme.Colors.TEXT_SECONDARY

        self.status_label.setText(
            message
        )

        self.status_label.setStyleSheet(
            f"""
            QLabel {{
                color:{color};
                font-size:9pt;
                font-weight:600;
            }}
            """
        )

    # ==========================================================
    # BUSY
    # ==========================================================

    def set_busy(
        self,
        busy
    ):

        self.search_button.setEnabled(
            not busy
        )

        self.invoice.setEnabled(
            not busy
        )

        self.date.setEnabled(
            not busy
        )