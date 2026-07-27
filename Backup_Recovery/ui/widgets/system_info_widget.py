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


class SystemInfoWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout()

        panel = PanelWidget(
            "Στοιχεία Συστήματος"
        )

        rows = [

            ("Όνομα Υπολογιστή", "--"),

            ("Λειτουργικό Σύστημα", "--"),

            ("Επεξεργαστής", "--"),

            ("Μνήμη RAM", "--"),

            ("Συνολικός Χώρος Δίσκου", "--"),

            ("Διαθέσιμος Χώρος Δίσκου", "--"),

            ("Έκδοση Sunsoft Backup", "1.0.0"),

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