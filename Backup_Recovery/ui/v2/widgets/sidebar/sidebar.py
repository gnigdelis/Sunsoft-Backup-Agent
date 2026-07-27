from PySide6.QtWidgets import QWidget, QVBoxLayout

from ui.v2.styles.theme import Theme

from ui.v2.widgets.sidebar.branding_widget import BrandingWidget
from ui.v2.widgets.sidebar.navigation_menu import NavigationMenu
from ui.v2.widgets.sidebar.status_widget import StatusWidget


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        self.setObjectName("Sidebar")

        self.setStyleSheet(f"""
            QWidget#Sidebar {{
                background: {Theme.Colors.SURFACE};
                border-right: 1px solid {Theme.Colors.BORDER};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(22)

        self.branding = BrandingWidget()

        self.menu = NavigationMenu()

        self.status = StatusWidget()

        layout.addWidget(self.branding)

        layout.addSpacing(12)

        layout.addWidget(self.menu)

        layout.addStretch()

        layout.addWidget(self.status)