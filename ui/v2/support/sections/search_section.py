from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDateEdit,
)

from PySide6.QtCore import QDate

from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.styles.theme import Theme


class SearchSection(BaseCard):

    search_clicked = Signal(
        int,
        str,
    )

    def __init__(self):

        super().__init__(

            title="Search Invoice",

            minimum_height=220,

        )

        self.build()

    def build(self):

        layout = QGridLayout()

        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(15)

        #
        # Invoice Number
        #

        invoice_label = QLabel(
            "Invoice Number"
        )

        self.invoice = QLineEdit()

        self.invoice.setPlaceholderText(
            "e.g. 2464592"
        )

        #
        # Date
        #

        date_label = QLabel(
            "Invoice Date"
        )

        self.date = QDateEdit()

        self.date.setCalendarPopup(True)

        self.date.setDate(
            QDate.currentDate()
        )

        self.date.setDisplayFormat(
            "dd/MM/yyyy"
        )

        #
        # Search
        #

        self.search = QPushButton(
            "Search"
        )

        self.search.clicked.connect(
            self.on_search
        )

        #
        # Layout
        #

        layout.addWidget(
            invoice_label,
            0,
            0,
        )

        layout.addWidget(
            self.invoice,
            0,
            1,
        )

        layout.addWidget(
            date_label,
            1,
            0,
        )

        layout.addWidget(
            self.date,
            1,
            1,
        )

        layout.addWidget(
            self.search,
            2,
            1,
        )

        self.content_layout.addLayout(
            layout
        )

    def on_search(self):

        text = self.invoice.text().strip()

        if not text.isdigit():

            return

        invoice = int(text)

        invoice_date = self.date.date().toString(
            "yyyyMMdd"
        )

        self.search_clicked.emit(

            invoice,

            invoice_date,

        )