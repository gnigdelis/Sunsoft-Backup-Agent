from PySide6.QtWidgets import (

    QWidget,
    QHBoxLayout,
    QStackedWidget,

)

from ui.styles.theme import (

    APPLICATION_BACKGROUND,

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

        #
        # APPLICATION SETTINGS
        #

        self.setWindowTitle(
            "Sunsoft Backup Agent"
        )

        #
        # UI FREEZE
        #
        # Το παράθυρο θα παραμένει
        # πάντα στα 1600x900.
        #

        self.setFixedSize(

            1600,
            900,

        )

        #
        # APPLICATION STYLE
        #

        self.setStyleSheet(

            f"""

            QWidget {{

                background-color: {APPLICATION_BACKGROUND};

            }}

            """

        )

        self.setup_ui()

    def setup_ui(self):

        #
        # MAIN LAYOUT
        #

        main_layout = QHBoxLayout()

        #
        # Δεν θέλουμε κενά μεταξύ
        # Sidebar και Dashboard.
        #

        main_layout.setContentsMargins(

            0,
            0,
            0,
            0,

        )

        main_layout.setSpacing(
            0
        )

        #
        # SIDEBAR
        #

        self.sidebar = SidebarWidget()

        #
        # STACKED WIDGET
        #

        self.stacked_widget = QStackedWidget()

        #
        # DASHBOARD STYLE
        #

        self.stacked_widget.setStyleSheet(

            f"""

            QStackedWidget {{

                background-color: {APPLICATION_BACKGROUND};
                border: none;

            }}

            """

        )

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

        #
        # SET LAYOUT
        #

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