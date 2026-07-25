from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)


class SettingsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        #
        # MAIN LAYOUT
        #

        main_layout = QVBoxLayout()

        #
        # BACKUP SETTINGS
        #

        backup_panel = PanelWidget(
            "Ρυθμίσεις Backup"
        )

        backup_panel.add_widget(
            QLabel("Cloud Backup")
        )

        backup_panel.add_widget(
            QLabel("Αυτόματο Backup")
        )

        backup_panel.add_widget(
            QLabel("Ειδοποιήσεις")
        )

        backup_panel.add_widget(
            QLabel("Φάκελος Backup")
        )

        #
        # COMPRESSION SETTINGS
        #

        compression_panel = PanelWidget(
            "Ρυθμίσεις Συμπίεσης"
        )

        compression_panel.add_widget(
            QLabel("ZIP")
        )

        compression_panel.add_widget(
            QLabel("7ZIP")
        )

        #
        # RETENTION SETTINGS
        #

        retention_panel = PanelWidget(
            "Διατήρηση Backup"
        )

        retention_panel.add_widget(
            QLabel("Ημέρες Διατήρησης")
        )

        #
        # APPLICATION SETTINGS
        #

        application_panel = PanelWidget(
            "Ρυθμίσεις Εφαρμογής"
        )

        application_panel.add_widget(
            QLabel("Έλεγχος Ενημερώσεων")
        )

        #
        # ADD PANELS
        #

        main_layout.addWidget(
            backup_panel
        )

        main_layout.addWidget(
            compression_panel
        )

        main_layout.addWidget(
            retention_panel
        )

        main_layout.addWidget(
            application_panel
        )

        main_layout.addStretch()

        #
        # SET LAYOUT
        #

        self.setLayout(
            main_layout
        )