from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from core.database.database_information import (
    DatabaseInformation,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)

from ui.widgets.common.info_row_widget import (
    InfoRowWidget,
)


class DatabaseInformationWidget(QWidget):

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
        # INFORMATION ROWS
        #

        self.sql_server = InfoRowWidget(
            "SQL Server",
            DatabaseInformation.get_sql_server(),
        )

        self.database_name = InfoRowWidget(
            "Όνομα Βάσης",
            DatabaseInformation.get_database_name(),
        )

        self.database_size = InfoRowWidget(
            "Μέγεθος Βάσης",
            DatabaseInformation.get_database_size(),
        )

        self.connection_status = InfoRowWidget(
            "Κατάσταση Σύνδεσης",
            DatabaseInformation.get_connection_status(),
        )

        self.last_sql_backup = InfoRowWidget(
            "Τελευταίο SQL Backup",
            DatabaseInformation.get_last_sql_backup(),
        )

        #
        # ADD ROWS
        #

        panel.add_widget(
            self.sql_server
        )

        panel.add_widget(
            self.database_name
        )

        panel.add_widget(
            self.database_size
        )

        panel.add_widget(
            self.connection_status
        )

        panel.add_widget(
            self.last_sql_backup
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