from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox,
)

from core.configuration.udl_locator import UDLLocator
from core.controllers.support_controller import SupportController

from ui.v2.widgets.header.header import Header
from ui.v2.widgets.footer.footer import Footer

from ui.v2.support.sections.search_section import SearchSection
from ui.v2.support.sections.results_section import ResultsSection
from ui.v2.support.sections.batch_section import BatchSection


class SupportLayout(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        #
        # Controller
        #

        self.controller = SupportController(

            UDLLocator.find()

        )

        self.connect_signals()

    def setup_ui(self):

        layout = QVBoxLayout(self)

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

    def connect_signals(self):

        #
        # Search
        #

        self.search.search_clicked.connect(

            self.controller.search_invoice

        )

        #
        # Reset
        #

        self.results.reset_clicked.connect(

            self.controller.reset_status

        )

        #
        # Search Result
        #

        self.controller.search_completed.connect(

            self.results.set_result

        )

        self.controller.search_failed.connect(

            self.on_search_failed

        )

        #
        # Reset Result
        #

        self.controller.reset_completed.connect(

            self.on_reset_completed

        )

        self.controller.reset_failed.connect(

            self.on_reset_failed

        )

    def on_search_failed(self, message):

        self.results.clear()

        QMessageBox.warning(

            self,

            "Search",

            message,

        )

    def on_reset_completed(self, result):

        QMessageBox.information(

            self,

            "Support",

            f"{result.affected_rows} record(s) updated.",

        )

    def on_reset_failed(self, message):

        QMessageBox.critical(

            self,

            "Support",

            message,

        )