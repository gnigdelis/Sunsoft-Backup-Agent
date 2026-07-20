from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class SystemInfoWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel(
                "SYSTEM INFO WIDGET"
            )
        )

        self.setLayout(layout)