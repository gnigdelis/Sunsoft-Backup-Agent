from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.v2.widgets.header.header import Header
from ui.v2.widgets.footer.footer import Footer

from ui.v2.dashboard.sections.summary_section import SummarySection
from ui.v2.dashboard.sections.operations_section import OperationsSection


class DashboardLayout(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        layout.setSpacing(
            15
        )

        self.header = Header()

        self.summary = SummarySection()

        self.operations = OperationsSection()

        self.footer = Footer()

        layout.addWidget(
            self.header
        )

        layout.addWidget(
            self.summary
        )

        layout.addWidget(
            self.operations
        )

        layout.addWidget(
            self.footer
        )

        self.setLayout(
            layout
        )