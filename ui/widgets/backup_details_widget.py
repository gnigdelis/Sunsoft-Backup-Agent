from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)

from ui.widgets.common.status_row_widget import (
    StatusRowWidget,
)


class BackupDetailsWidget(QWidget):

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
            "Λεπτομέρειες Backup"
        )

        #
        # BACKUP PIPELINE
        #

        backup_operations = [

            ("Έλεγχος Αρχείων", "ΣΕ ΑΝΑΜΟΝΗ", "--:--:--"),

            ("Αντιγραφή Αρχείων", "ΣΕ ΑΝΑΜΟΝΗ", "--:--:--"),

            ("Εξαγωγή Registry", "ΣΕ ΑΝΑΜΟΝΗ", "--:--:--"),

            ("Backup Βάσης Δεδομένων", "ΣΕ ΑΝΑΜΟΝΗ", "--:--:--"),

            ("Δημιουργία Manifest", "ΣΕ ΑΝΑΜΟΝΗ", "--:--:--"),

            ("Συμπίεση (7z)", "ΣΕ ΑΝΑΜΟΝΗ", "--:--:--"),

            ("Μεταφόρτωση", "ΣΕ ΑΝΑΜΟΝΗ", "--:--:--"),

        ]

        #
        # CREATE STATUS ROWS
        #

        for title, status, duration in backup_operations:

            row = StatusRowWidget(
                title=title,
                status=status,
                duration=duration,
            )

            panel.add_widget(
                row
            )

        #
        # TOTAL BACKUP TIME
        #

        self.total_time_title = QLabel(
            "Συνολικός Χρόνος Backup"
        )

        self.total_time_value = QLabel(
            "--:--:--"
        )

        panel.add_widget(
            self.total_time_title
        )

        panel.add_widget(
            self.total_time_value
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