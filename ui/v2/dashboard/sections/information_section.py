from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class InformationSection(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Information Section")
        )

        self.setLayout(layout)