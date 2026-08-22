from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.v2.support.widgets.amvrosia_repair_card import (
    AmvrosiaRepairCard,
)


class SupportPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        layout.setSpacing(20)

        self.repair_card = AmvrosiaRepairCard()

        layout.addWidget(
            self.repair_card
        )

        layout.addStretch()