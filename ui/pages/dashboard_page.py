from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.widgets.header_widget import (
    HeaderWidget,
)

from ui.panels.summary_panel import (
    SummaryPanel,
)

from ui.panels.information_panel import (
    InformationPanel,
)

from ui.panels.operations_panel import (
    OperationsPanel,
)

from ui.widgets.footer_widget import (
    FooterWidget,
)


class DashboardPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout()

        #
        # DASHBOARD MARGINS
        #

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        #
        # DASHBOARD SPACING
        #

        main_layout.setSpacing(
            15
        )

        #
        # HEADER
        #

        main_layout.addWidget(
            HeaderWidget()
        )

        #
        # SUMMARY PANEL
        #

        main_layout.addWidget(
            SummaryPanel()
        )

        #
        # INFORMATION PANEL
        #

        main_layout.addWidget(
            InformationPanel()
        )

        #
        # OPERATIONS PANEL
        #

        main_layout.addWidget(
            OperationsPanel()
        )

        #
        # FOOTER
        #

        main_layout.addWidget(
            FooterWidget()
        )

        #
        # IMPORTANT !!!
        #
        # Δεν βάζουμε addStretch()
        # Δεν βάζουμε ScrollArea ακόμη.
        #

        self.setLayout(
            main_layout
        )