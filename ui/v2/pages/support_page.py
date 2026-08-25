from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.v2.support.layouts.support_layout import SupportLayout


class SupportPage(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            0
        )

        layout.addWidget(
            SupportLayout()
        )