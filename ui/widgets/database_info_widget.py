from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)

from ui.widgets.common.info_row_widget import (
    InfoRowWidget,
)


class DatabaseInfoWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        #
        # MAIN LAYOUT
        #

        main_layout = QVBoxLayout()

        #
        # PANEL
        #

        panel = PanelWidget(
            "Στοιχεία Βάσης Δεδομένων"
        )

        #
        # DATABASE INFORMATION
        #

        database_information = [

            ("Τύπος Βάσης", "N/A"),

            ("Όνομα Server", "N/A"),

            ("Όνομα Βάσης", "N/A"),

            ("Κατάσταση Σύνδεσης", "N/A"),

            ("Τελευταίος Έλεγχος", "N/A"),

            ("Έκδοση SQL Server", "N/A"),

            ("Μέγεθος Βάσης", "N/A"),

            ("Κατάσταση Backup", "N/A"),

        ]

        #
        # CREATE INFO ROWS
        #

        for title, value in database_information:

            row = InfoRowWidget(
                title=title,
                value=value,
            )

            panel.add_widget(
                row
            )

        #
        # ADD PANEL
        #

        main_layout.addWidget(
            panel
        )

        #
        # SET LAYOUT
        #

        self.setLayout(
            main_layout
        )