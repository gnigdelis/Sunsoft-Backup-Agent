from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class SummaryWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("SUMMARY WIDGET")
        )

        self.setLayout(layout)