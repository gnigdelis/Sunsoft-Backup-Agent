from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from core.system.system_information import (
    SystemInformation,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)

from ui.widgets.common.info_row_widget import (
    InfoRowWidget,
)


class SystemInformationWidget(QWidget):

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
        # INFORMATION ROWS
        #

        self.computer_name = InfoRowWidget(
            "Όνομα Υπολογιστή",
            SystemInformation.get_computer_name(),
        )

        self.windows_version = InfoRowWidget(
            "Windows Version",
            SystemInformation.get_windows_version(),
        )

        self.processor = InfoRowWidget(
            "Επεξεργαστής",
            SystemInformation.get_processor(),
        )

        self.ram = InfoRowWidget(
            "RAM",
            SystemInformation.get_ram(),
        )

        self.free_disk_space = InfoRowWidget(
            "Ελεύθερος Χώρος",
            SystemInformation.get_free_disk_space(),
        )

        #
        # ADD ROWS
        #

        panel.add_widget(
            self.computer_name
        )

        panel.add_widget(
            self.windows_version
        )

        panel.add_widget(
            self.processor
        )

        panel.add_widget(
            self.ram
        )

        panel.add_widget(
            self.free_disk_space
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