from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

from ui.styles.config import (
    APPLICATION_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
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


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        #
        # WINDOW SETTINGS
        #

        self.setWindowTitle(
            APPLICATION_NAME
        )

        self.setFixedSize(

            WINDOW_WIDTH,
            WINDOW_HEIGHT,

        )

        #
        # MAIN LAYOUT
        #

        main_layout = QHBoxLayout()

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

        self.sidebar_widget = (
            SidebarWidget()
        )

        self.sidebar_widget.setFixedWidth(
            280
        )

        #
        # DASHBOARD
        #

        self.dashboard_page = (
            DashboardPage()
        )

        #
        # ADD WIDGETS
        #

        main_layout.addWidget(
            self.sidebar_widget
        )

        main_layout.addWidget(
            self.dashboard_page,
            1
        )

        #
        # SET LAYOUT
        #

        self.setLayout(
            main_layout
        )

        #
        # APPLICATION THEME
        #

        self.setStyleSheet(

            f"""

            QWidget {{

                background-color:
                    {APPLICATION_BACKGROUND};

            }}

            """

        )