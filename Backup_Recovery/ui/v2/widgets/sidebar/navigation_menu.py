from PySide6.QtWidgets import QVBoxLayout, QWidget

from ui.v2.styles.theme import Theme
from ui.v2.widgets.sidebar.navigation_item import NavigationItem


class NavigationMenu(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.dashboard = NavigationItem(
            "Dashboard",
            "🏠",
            "#e53935",
            True,
        )

        self.backup = NavigationItem(
            "Backup",
            "💾",
            "#8e24aa",
        )

        self.restore = NavigationItem(
            "Restore",
            "♻",
            "#43a047",
        )

        self.history = NavigationItem(
            "History",
            "🕒",
            "#1e88e5",
        )

        self.logs = NavigationItem(
            "Logs",
            "📄",
            "#757575",
        )

        self.settings = NavigationItem(
            "Settings",
            "⚙",
            "#fb8c00",
        )

        layout.addWidget(self.dashboard)
        layout.addWidget(self.backup)
        layout.addWidget(self.restore)
        layout.addWidget(self.history)
        layout.addWidget(self.logs)
        layout.addWidget(self.settings)

        layout.addStretch()

        self.items = [
            self.dashboard,
            self.backup,
            self.restore,
            self.history,
            self.logs,
            self.settings,
        ]

        for item in self.items:
            item.clicked.connect(
                lambda _, current=item: self.set_active(current)
            )

    def set_active(self, current):

        for item in self.items:
            item.setActive(item == current)