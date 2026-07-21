from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)


class HeaderWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QHBoxLayout()

        #
        # LEFT SIDE
        #

        left_layout = QVBoxLayout()

        self.title_label = QLabel(
            "Golden Backup"
        )

        self.subtitle_label = QLabel(
            "Πλήρες backup αρχείων, Registry και βάσης δεδομένων"
        )

        left_layout.addWidget(
            self.title_label
        )

        left_layout.addWidget(
            self.subtitle_label
        )

        #
        # RIGHT SIDE
        #

        right_layout = QVBoxLayout()

        self.datetime_label = QLabel(
            "20/07/2026 16:45"
        )

        self.version_label = QLabel(
            "Version 1.0.0.0"
        )

        right_layout.addWidget(
            self.datetime_label
        )

        right_layout.addWidget(
            self.version_label
        )

        #
        # ADD LAYOUTS
        #

        main_layout.addLayout(
            left_layout,
            4
        )

        main_layout.addLayout(
            right_layout,
            1
        )

        self.setLayout(
            main_layout
        )