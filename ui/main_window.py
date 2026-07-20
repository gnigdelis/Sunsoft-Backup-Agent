from PySide6.QtWidgets import (

    QWidget,
    QHBoxLayout,
    QStackedWidget,

)

from ui.widgets.sidebar_widget import (
    SidebarWidget,
)

from ui.pages.dashboard_page import (
    DashboardPage,
)

from ui.pages.backup_page import (
    BackupPage,
)


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Sunsoft Golden Backup Tool"
        )

        self.resize(
            1600,
            900,
        )

        self.setup_ui()

    def setup_ui(self):

        main_layout = QHBoxLayout()

        #
        # SIDEBAR
        #

        self.sidebar = SidebarWidget()

        #
        # STACKED WIDGET
        #

        self.stacked_widget = QStackedWidget()

        #
        # PAGES
        #

        self.dashboard_page = DashboardPage()

        self.backup_page = BackupPage()

        #
        # ADD PAGES
        #

        self.stacked_widget.addWidget(
            self.dashboard_page
        )

        self.stacked_widget.addWidget(
            self.backup_page
        )

        #
        # NAVIGATION
        #

        self.sidebar.dashboard_button.clicked.connect(
            self.show_dashboard
        )

        self.sidebar.backup_button.clicked.connect(
            self.show_backup
        )

        #
        # MAIN LAYOUT
        #

        main_layout.addWidget(
            self.sidebar,
            1,
        )

        main_layout.addWidget(
            self.stacked_widget,
            5,
        )

        self.setLayout(
            main_layout
        )

    def show_dashboard(self):

        self.stacked_widget.setCurrentWidget(
            self.dashboard_page
        )

    def show_backup(self):

        self.stacked_widget.setCurrentWidget(
            self.backup_page
        )