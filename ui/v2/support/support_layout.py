from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.v2.widgets.header.header import Header
from ui.v2.widgets.footer.footer import Footer

from ui.v2.support.sections.search_section import SearchSection
from ui.v2.support.sections.results_section import ResultsSection
from ui.v2.support.sections.batch_section import BatchSection


class SupportLayout(QWidget):

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

        layout.setSpacing(15)

        self.header = Header()

        self.search = SearchSection()

        self.results = ResultsSection()

        self.batch = BatchSection()

        self.footer = Footer()

        layout.addWidget(self.header)
        layout.addWidget(self.search)
        layout.addWidget(self.results)
        layout.addWidget(self.batch)
        layout.addWidget(self.footer)

        self.setLayout(layout)