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
from ui.v2.pages.restore_page import RestorePage
from ui.v2.pages.history_page import HistoryPage
from ui.v2.pages.mydata.mydata_sent_page import MyDataSentPage
from ui.v2.pages.support_page import SupportPage

from ui.v2.pages.database_maintenance_page import (
    DatabaseMaintenancePage,
)

from ui.v2.pages.settings_page import SettingsPage


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.setup_navigation()

    def setup_ui(self):

        self.setWindowTitle(
            "Sunsoft Support Agent v2.0"
        )

        try:

            self.setWindowIcon(
                QIcon("assets/icons/app.ico")
            )

        except Exception:

            pass

        self.resize(
            1700,
            980,
        )

        self.setMinimumSize(
            1450,
            900,
        )

        self.setObjectName(
            "MainWindow"
        )

        self.setStyleSheet(
            Theme.stylesheet()
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            0
        )

        #
        # Sidebar
        #

        self.sidebar = Sidebar()

        self.sidebar.setFixedWidth(
            300
        )

        #
        # Page stack
        #

        self.stack = QStackedWidget()

        self.navigation = NavigationManager(
            self.stack
        )

        #
        # Pages
        #

        self.dashboard_page = (
            DashboardPage()
        )

        self.backup_page = (
            BackupPage()
        )

        self.restore_page = (
            RestorePage()
        )

        self.history_page = (
            HistoryPage()
        )

        self.mydata_sent_page = (
            MyDataSentPage()
        )

        self.support_page = (
            SupportPage()
        )

        self.database_maintenance_page = (
            DatabaseMaintenancePage()
        )

        self.settings_page = (
            SettingsPage()
        )

        #
        # Register pages
        #

        self.navigation.register(
            "dashboard",
            self.dashboard_page,
        )

        self.navigation.register(
            "backup",
            self.backup_page,
        )

        self.navigation.register(
            "restore",
            self.restore_page,
        )

        self.navigation.register(
            "history",
            self.history_page,
        )

        self.navigation.register(
            "mydata_sent",
            self.mydata_sent_page,
        )

        self.navigation.register(
            "support",
            self.support_page,
        )

        self.navigation.register(
            "database_maintenance",
            self.database_maintenance_page,
        )

        self.navigation.register(
            "settings",
            self.settings_page,
        )

        #
        # Main layout
        #

        layout.addWidget(
            self.sidebar
        )

        layout.addWidget(
            self.stack,
            1,
        )

    def setup_navigation(self):

        #
        # Default page
        #

        self.navigation.show(
            "dashboard"
        )

        #
        # Dashboard
        #

        self.sidebar.menu.dashboard.clicked.connect(
            lambda: self.navigation.show(
                "dashboard"
            )
        )

        #
        # Backup
        #

        self.sidebar.menu.backup.clicked.connect(
            lambda: self.navigation.show(
                "backup"
            )
        )

        #
        # Restore
        #

        self.sidebar.menu.restore.clicked.connect(
            lambda: self.navigation.show(
                "restore"
            )
        )

        #
        # History
        #

        self.sidebar.menu.history.clicked.connect(
            lambda: self.navigation.show(
                "history"
            )
        )

        #
        # MyData Sent
        #

        self.sidebar.menu.mydata_sent.clicked.connect(
            lambda: self.navigation.show(
                "mydata_sent"
            )
        )

        #
        # Support
        #

        self.sidebar.menu.support.clicked.connect(
            lambda: self.navigation.show(
                "support"
            )
        )

        #
        # Delete / Rebuild / Shrink
        #

        self.sidebar.menu.database_maintenance.clicked.connect(
            lambda: self.navigation.show(
                "database_maintenance"
            )
        )

        #
        # Settings
        #

        self.sidebar.menu.settings.clicked.connect(
            lambda: self.navigation.show(
                "settings"
            )
        )