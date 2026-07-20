from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class ActionButtonsWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel(
                "ACTION BUTTONS WIDGET"
            )
        )

        self.setLayout(layout)