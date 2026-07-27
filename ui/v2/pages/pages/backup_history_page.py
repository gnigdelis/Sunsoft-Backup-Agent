from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)


class BackupHistoryPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout()

        #
        # HISTORY PANEL
        #

        history_panel = PanelWidget(
            "Ιστορικό Backup"
        )

        history_panel.add_widget(
            QLabel(
                "Ημερομηνία : --"
            )
        )

        history_panel.add_widget(
            QLabel(
                "Μέγεθος Backup : --"
            )
        )

        history_panel.add_widget(
            QLabel(
                "Διάρκεια : --"
            )
        )

        history_panel.add_widget(
            QLabel(
                "Κατάσταση : --"
            )
        )

        history_panel.add_widget(
            QLabel(
                "Τοποθεσία Backup : --"
            )
        )

        #
        # BUTTONS
        #

        self.open_backup_button = QPushButton(
            "Άνοιγμα Backup"
        )

        self.delete_backup_button = QPushButton(
            "Διαγραφή Backup"
        )

        history_panel.add_widget(
            self.open_backup_button
        )

        history_panel.add_widget(
            self.delete_backup_button
        )

        #
        # STATISTICS PANEL
        #

        statistics_panel = PanelWidget(
            "Στατιστικά Backup"
        )

        statistics_panel.add_widget(
            QLabel(
                "Συνολικά Backup : 0"
            )
        )

        statistics_panel.add_widget(
            QLabel(
                "Τελευταίο Backup : --"
            )
        )

        #
        # ADD PANELS
        #

        main_layout.addWidget(
            history_panel
        )

        main_layout.addWidget(
            statistics_panel
        )

        main_layout.addStretch()

        self.setLayout(
            main_layout
        )