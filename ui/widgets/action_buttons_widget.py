from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)


class ActionButtonsWidget(QWidget):

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
            "Ενέργειες Backup"
        )

        #
        # BUTTONS
        #

        self.start_backup_button = QPushButton(
            "Έναρξη Backup"
        )

        self.validate_button = QPushButton(
            "Έλεγχος Ρυθμίσεων"
        )

        self.open_backup_folder_button = QPushButton(
            "Άνοιγμα Φακέλου Backup"
        )

        #
        # BUTTON HEIGHT
        #

        self.start_backup_button.setMinimumHeight(
            45
        )

        self.validate_button.setMinimumHeight(
            45
        )

        self.open_backup_folder_button.setMinimumHeight(
            45
        )

        #
        # ADD BUTTONS
        #

        panel.add_widget(
            self.start_backup_button
        )

        panel.add_widget(
            self.validate_button
        )

        panel.add_widget(
            self.open_backup_folder_button
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