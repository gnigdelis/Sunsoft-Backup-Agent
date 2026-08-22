from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)

from core.controllers.amvrosia_controller import (
    AmvrosiaController,
)

from ui.v2.widgets.cards.base_card import BaseCard


class AmvrosiaRepairCard(BaseCard):

    def __init__(self):

        super().__init__(
            "Repair Amvrosia Order",
            320,
        )

        self.controller = AmvrosiaController()

        self.current_order = None

        self.build()
        self.connect_signals()

    def build(self):

        self.order = QLineEdit()

        self.order.setPlaceholderText(
            "Enter Amvrosia Order Number"
        )

        self.search_button = QPushButton(
            "Search"
        )

        self.repair_button = QPushButton(
            "Repair Order"
        )

        self.repair_button.setEnabled(False)

        self.status_label = QLabel(
            "Waiting for order..."
        )

        self.details_label = QLabel(
            ""
        )

        self.content_layout.addWidget(
            QLabel("Order Number")
        )

        self.content_layout.addWidget(
            self.order
        )

        buttons = QHBoxLayout()

        buttons.addWidget(
            self.search_button
        )

        buttons.addWidget(
            self.repair_button
        )

        self.content_layout.addLayout(
            buttons
        )

        self.content_layout.addSpacing(
            15
        )

        self.content_layout.addWidget(
            self.status_label
        )

        self.content_layout.addWidget(
            self.details_label
        )

    def connect_signals(self):

        self.search_button.clicked.connect(
            self.on_search
        )

        self.repair_button.clicked.connect(
            self.on_repair
        )

        self.controller.search_completed.connect(
            self.on_search_completed
        )

        self.controller.repair_completed.connect(
            self.on_repair_completed
        )

        self.controller.failed.connect(
            self.on_failed
        )

    def on_search(self):

        order_number = self.order.text().strip()

        self.current_order = None

        self.repair_button.setEnabled(
            False
        )

        if not order_number.isdigit():

            self.status_label.setText(
                "Enter a valid order number."
            )

            self.details_label.setText(
                ""
            )

            return

        self.search_button.setEnabled(
            False
        )

        self.status_label.setText(
            "Searching order..."
        )

        self.details_label.setText(
            ""
        )

        self.controller.search_order(
            int(order_number)
        )

    def on_repair(self):

        if self.current_order is None:

            return

        order_number = self.order.text().strip()

        if not order_number.isdigit():

            return

        self.search_button.setEnabled(
            False
        )

        self.repair_button.setEnabled(
            False
        )

        self.status_label.setText(
            "Repairing order..."
        )

        self.controller.repair_order(
            int(order_number)
        )

    def on_search_completed(
        self,
        result,
    ):

        self.search_button.setEnabled(
            True
        )

        if not result.found:

            self.current_order = None

            self.repair_button.setEnabled(
                False
            )

            self.status_label.setText(
                "Order not found."
            )

            self.details_label.setText(
                result.message
            )

            return

        self.current_order = result

        self.details_label.setText(
            f"Order: {result.order_number}\n"
            f"Total Lines: {result.total_rows}\n"
            f"Status 1: {result.status_1}\n"
            f"Status 0: {result.status_0}\n"
            f"Status 2: {result.status_2}"
        )

        if result.repairable > 0:

            self.status_label.setText(
                f"⚠ {result.repairable} "
                f"γραμμές χρειάζονται διόρθωση."
            )

            self.repair_button.setEnabled(
                True
            )

        else:

            self.status_label.setText(
                "✔ Η παραγγελία είναι ολοκληρωμένη."
            )

            self.repair_button.setEnabled(
                False
            )

    def on_repair_completed(
        self,
        result,
    ):

        self.search_button.setEnabled(
            True
        )

        self.repair_button.setEnabled(
            False
        )

        if result.success:

            self.status_label.setText(
                "✔ Η παραγγελία διορθώθηκε επιτυχώς."
            )

            self.details_label.setText(
                f"Order: {result.order_number}\n"
                f"Updated Lines: "
                f"{result.updated_rows}\n"
                f"Remaining Status 0/2: "
                f"{result.remaining_rows}"
            )

            self.current_order = None

        else:

            self.status_label.setText(
                "✖ Repair failed."
            )

            self.details_label.setText(
                result.message
            )

    def on_failed(
        self,
        message,
    ):

        self.search_button.setEnabled(
            True
        )

        self.repair_button.setEnabled(
            False
        )

        self.status_label.setText(
            "✖ Repair failed."
        )

        self.details_label.setText(
            message
        )