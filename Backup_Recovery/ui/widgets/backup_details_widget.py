from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)

from ui.widgets.common.info_row_widget import (
    InfoRowWidget,
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
            "Στοιχεία Backup"
        )

        #
        # INFORMATION ROWS
        #

        self.cloud_backup = InfoRowWidget(
            "Cloud Backup",
            "Απενεργοποιημένο",
        )

        self.scheduler = InfoRowWidget(
            "Scheduler",
            "Απενεργοποιημένος",
        )

        self.notifications = InfoRowWidget(
            "Notifications",
            "Απενεργοποιημένες",
        )

        self.destination = InfoRowWidget(
            "Προορισμός",
            "Δεν έχει οριστεί",
        )

        self.compression = InfoRowWidget(
            "Συμπίεση",
            "ZIP",
        )

        #
        # ADD WIDGETS
        #

        panel.add_widget(
            self.cloud_backup
        )

        panel.add_widget(
            self.scheduler
        )

        panel.add_widget(
            self.notifications
        )

        panel.add_widget(
            self.destination
        )

        panel.add_widget(
            self.compression
        )

        #
        # ADD PANEL
        #

        main_layout.addWidget(
            panel
        )

        self.setLayout(
            main_layout
        )