from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class FooterWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel(
                "FOOTER WIDGET"
            )
        )

        self.setLayout(layout)