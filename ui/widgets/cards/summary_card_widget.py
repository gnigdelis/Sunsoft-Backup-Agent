from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class SummaryCardWidget(QWidget):

    def __init__(
        self,
        title: str,
        value: str,
        status: str = "",
    ):

        super().__init__()

        layout = QVBoxLayout()

        self.title_label = QLabel(
            title
        )

        self.value_label = QLabel(
            value
        )

        self.status_label = QLabel(
            status
        )

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.value_label
        )

        layout.addWidget(
            self.status_label
        )

        self.setLayout(
            layout
        )