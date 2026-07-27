from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from ui.v2.styles.theme import Theme

from ui.v2.navigation.navigation_manager import NavigationManager

from ui.v2.widgets.sidebar.sidebar import Sidebar

from ui.v2.pages.dashboard_page import DashboardPage
from ui.v2.pages.backup_page import BackupPage
from ui.v2.pages.logs_page import LogsPage
from ui.v2.pages.settings_page import SettingsPage
from ui.v2.pages.restore_page import RestorePage
from ui.v2.pages.history_page import HistoryPage


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.setup_navigation()

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
        # Stack
        #

        self.stack = QStackedWidget()

        #
        # Navigation
        #

        self.navigation = NavigationManager(
            self.stack
        )

        #
        # Pages
        #

        self.dashboard_page = DashboardPage()
        self.backup_page = BackupPage()
        self.logs_page = LogsPage()
        self.settings_page = SettingsPage()
        self.restore_page = RestorePage()
        self.history_page = HistoryPage()

        self.navigation.register(
            "dashboard",
            self.dashboard_page
        )

        self.navigation.register(
            "backup",
            self.backup_page
        )

        self.navigation.register(
            "logs",
            self.logs_page
        )

        self.navigation.register(
            "settings",
            self.settings_page
        )

        self.navigation.register(
            "restore",
            self.restore_page
        )

        self.navigation.register(
            "history",
            self.history_page
        )

        layout.addWidget(
            self.sidebar
        )

        layout.addWidget(
            self.stack,
            1,
        )

    def setup_navigation(self):

        #
        # προσωρινά
        #

        self.navigation.show(
            "dashboard"
        )