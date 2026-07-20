from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class BackupPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel(
                "BACKUP PAGE"
            )
        )

        self.setLayout(
            layout
        )