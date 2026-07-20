from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class BackupDetailsWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel(
                "BACKUP DETAILS WIDGET"
            )
        )

        self.setLayout(layout)