from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class DatabaseInfoWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel(
                "DATABASE INFO WIDGET"
            )
        )

        self.setLayout(layout)