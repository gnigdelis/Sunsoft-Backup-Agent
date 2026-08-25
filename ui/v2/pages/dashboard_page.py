from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.v2.dashboard.layouts.dashboard_layout import DashboardLayout


class DashboardPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            DashboardLayout()
        )

        self.setLayout(
            layout
        )