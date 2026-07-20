from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class HeaderWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        self.title = QLabel(
            "Golden Backup"
        )

        self.subtitle = QLabel(
            "Πλήρες backup αρχείων, Registry και βάσης δεδομένων."
        )

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

        self.setLayout(layout)