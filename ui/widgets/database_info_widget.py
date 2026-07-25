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

        main_layout = QVBoxLayout()

        panel = PanelWidget(
            "Στοιχεία Βάσης Δεδομένων"
        )

        rows = [

            ("Τύπος Βάσης", "SQL Server"),

            ("Όνομα Βάσης", "--"),

            ("Κατάσταση Σύνδεσης", "--"),

            ("Τελευταίος Έλεγχος", "--"),

            ("Μέγεθος Βάσης", "--"),

            ("Κατάσταση Backup", "--"),

        ]

        for title, value in rows:

            panel.add_widget(

                InfoRowWidget(
                    title,
                    value,
                )

            )

        main_layout.addWidget(
            panel
        )

        self.setLayout(
            main_layout
        )