from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
)

from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.styles.theme import Theme


class ResultsSection(BaseCard):

    reset_clicked = Signal(int)

    def __init__(self):

        super().__init__(

            title="Search Result",

            minimum_height=220,

        )

        self.current_oid = None

        self.build()

    def build(self):

        self.invoice = QLabel("-")

        self.oid = QLabel("-")

        self.status = QLabel("-")

        self.invoice.setFont(
            Theme.Typography.heading()
        )

        self.oid.setFont(
            Theme.Typography.heading()
        )

        self.status.setFont(
            Theme.Typography.heading()
        )

        self.content_layout.addWidget(
            QLabel("Invoice")
        )

        self.content_layout.addWidget(
            self.invoice
        )

        self.content_layout.addSpacing(10)

        self.content_layout.addWidget(
            QLabel("OID")
        )

        self.content_layout.addWidget(
            self.oid
        )

        self.content_layout.addSpacing(10)

        self.content_layout.addWidget(
            QLabel("Status")
        )

        self.content_layout.addWidget(
            self.status
        )

        self.content_layout.addSpacing(20)

        self.reset_button = QPushButton(

            "Reset Status"

        )

        self.reset_button.setEnabled(
            False
        )

        self.reset_button.clicked.connect(
            self.on_reset
        )

        self.content_layout.addWidget(
            self.reset_button
        )

    def set_result(self, result):

        self.current_oid = result.oid

        self.invoice.setText(

            str(

                result.data["SalesTransNoteNo"]

            )

        )

        self.oid.setText(

            str(

                result.oid

            )

        )

        self.status.setText(

            str(

                result.status

            )

        )

        self.reset_button.setEnabled(
            True
        )

    def clear(self):

        self.current_oid = None

        self.invoice.setText("-")

        self.oid.setText("-")

        self.status.setText("-")

        self.reset_button.setEnabled(
            False
        )

    def on_reset(self):

        if self.current_oid is None:

            return

        self.reset_clicked.emit(

            self.current_oid

        )