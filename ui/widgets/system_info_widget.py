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

        #
        # MAIN LAYOUT
        #

        main_layout = QVBoxLayout()

        #
        # PANEL
        #

        panel = PanelWidget(
            "Στοιχεία Συστήματος"
        )

        #
        # SYSTEM INFORMATION
        #

        system_information = [

            ("Όνομα Υπολογιστή", "N/A"),

            ("Τρέχων Χρήστης", "N/A"),

            ("Έκδοση Windows", "N/A"),

            ("Επεξεργαστής", "N/A"),

            ("Μνήμη RAM", "N/A"),

            ("Συνολικός Χώρος Δίσκου", "N/A"),

            ("Ελεύθερος Χώρος Δίσκου", "N/A"),

            ("Έκδοση Agent", "1.0.0"),

        ]

        #
        # CREATE INFO ROWS
        #

        for title, value in system_information:

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