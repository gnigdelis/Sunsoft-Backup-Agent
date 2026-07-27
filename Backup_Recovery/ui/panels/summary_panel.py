from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

from ui.widgets.cards.summary_card_widget import (
    SummaryCardWidget,
)


class SummaryPanel(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        #
        # MAIN LAYOUT
        #

        main_layout = QVBoxLayout()

        #
        # PANEL CONTAINER
        #

        panel_frame = QFrame()

        panel_layout = QHBoxLayout()

        panel_layout.setSpacing(
            20
        )

        panel_layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        #
        # SUMMARY CARDS
        #

        self.last_backup_card = SummaryCardWidget(
            title="Τελευταίο Backup",
            value="ΠΟΤΕ",
            status="ΑΝΑΜΟΝΗ",
        )

        self.files_card = SummaryCardWidget(
            title="Αρχεία Backup",
            value="0",
            status="ΑΝΑΜΟΝΗ",
        )

        self.database_card = SummaryCardWidget(
            title="Βάση Δεδομένων",
            value="0",
            status="ΑΝΑΜΟΝΗ",
        )

        self.backup_size_card = SummaryCardWidget(
            title="Μέγεθος Backup",
            value="0 MB",
            status="ΑΝΑΜΟΝΗ",
        )

        self.status_card = SummaryCardWidget(
            title="Κατάσταση Backup",
            value="ΕΤΟΙΜΟ",
            status="ΑΝΑΜΟΝΗ",
        )

        #
        # ADD CARDS
        #

        panel_layout.addWidget(
            self.last_backup_card
        )

        panel_layout.addWidget(
            self.files_card
        )

        panel_layout.addWidget(
            self.database_card
        )

        panel_layout.addWidget(
            self.backup_size_card
        )

        panel_layout.addWidget(
            self.status_card
        )

        #
        # SET PANEL LAYOUT
        #

        panel_frame.setLayout(
            panel_layout
        )

        #
        # ADD PANEL
        #

        main_layout.addWidget(
            panel_frame
        )

        self.setLayout(
            main_layout
        )