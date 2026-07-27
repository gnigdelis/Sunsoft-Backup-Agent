from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from ui.v2.styles.theme import Theme

from ui.v2.widgets.sidebar.sidebar import Sidebar

from ui.v2.pages.dashboard_page import DashboardPage


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle("Sunsoft Support Agent v2.0")

        try:
            self.setWindowIcon(
                QIcon("assets/icons/app.ico")
            )
        except Exception:
            pass

        self.resize(1700, 980)
        self.setMinimumSize(1450, 900)

        self.setObjectName("MainWindow")
        self.setStyleSheet(
            Theme.stylesheet()
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        #
        # Sidebar
        #

        self.sidebar = Sidebar()
        self.sidebar.setFixedWidth(300)

        #
        # Pages
        #

        self.stack = QStackedWidget()

        self.dashboard_page = DashboardPage()

        self.stack.addWidget(
            self.dashboard_page
        )

        #
        # Layout
        #

        layout.addWidget(
            self.sidebar
        )

        layout.addWidget(
            self.stack,
            1,
        )