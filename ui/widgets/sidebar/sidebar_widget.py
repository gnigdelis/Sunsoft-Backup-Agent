from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.styles.theme import (
    SIDEBAR_BACKGROUND,
)

from ui.widgets.sidebar.sidebar_logo import (
    SidebarLogo,
)

from ui.widgets.sidebar.sidebar_menu import (
    SidebarMenu,
)

from ui.widgets.sidebar.sidebar_status import (
    SidebarStatus,
)


class SidebarWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            20,
            24,
            20,
            24,
        )

        layout.setSpacing(
            24
        )

        #
        # LOGO
        #

        self.logo_widget = SidebarLogo()

        #
        # MENU
        #

        self.menu_widget = SidebarMenu()

        #
        # STATUS
        #

        self.status_widget = SidebarStatus()

        #
        # LAYOUT
        #

        layout.addWidget(
            self.logo_widget
        )

        layout.addSpacing(
            10
        )

        layout.addWidget(
            self.menu_widget
        )

        layout.addStretch()

        layout.addWidget(
            self.status_widget
        )

        self.setLayout(
            layout
        )

    def setup_styles(self):

        self.setStyleSheet(

            f"""

            QWidget {{

                background-color: {SIDEBAR_BACKGROUND};

            }}

            """

        )