from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
)


class SidebarWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        self.dashboard_button = QPushButton(
            "Dashboard"
        )

        self.backup_button = QPushButton(
            "Backup Now"
        )

        self.restore_button = QPushButton(
            "Restore"
        )

        self.backups_button = QPushButton(
            "Backups"
        )

        self.settings_button = QPushButton(
            "Settings"
        )

        self.logs_button = QPushButton(
            "Logs"
        )

        self.about_button = QPushButton(
            "About"
        )

        buttons = [

            self.dashboard_button,
            self.backup_button,
            self.restore_button,
            self.backups_button,
            self.settings_button,
            self.logs_button,
            self.about_button,

        ]

        for button in buttons:

            button.setMinimumHeight(
                50
            )

            layout.addWidget(
                button
            )

        layout.addStretch()

        self.setLayout(
            layout
        )