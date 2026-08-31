from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from ui.v2.widgets.sidebar.navigation_item import NavigationItem
from core.security.technical_access import TechnicalAccess


class NavigationMenu(QWidget):

    def __init__(self):

        super().__init__()

        self.items = []

        self.setup_ui()

        self.update_technical_access()

        TechnicalAccess().access_changed.connect(
            self.update_technical_access
        )

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            10
        )

        menu_items = [

            (
                "Dashboard",
                "dashboard.svg",
                "#e53935",
                True,
            ),

            (
                "Backup",
                "backup.svg",
                "#8e24aa",
                False,
            ),

            (
                "Restore",
                "restore.svg",
                "#43a047",
                False,
            ),

            (
                "Empty Lock",
                "history.svg",
                "#1e88e5",
                False,
            ),

            (
                "Delete Pending Order",
                "logs.svg",
                "#00acc1",
                False,
            ),

            (
                "myDATA Manager",
                "logs.svg",
                "#757575",
                False,
            ),

            (
                "Settings",
                "settings.svg",
                "#fb8c00",
                False,
            ),

            (
                "SQL Tools",
                "database.svg",
                "#8e24aa",
                False,
            ),
        ]

        for text, icon, color, active in menu_items:

            item = NavigationItem(
                text=text,
                icon=icon,
                color=color,
                active=active,
            )

            item.clicked.connect(
                lambda current=item:
                self.set_active(
                    current
                )
            )

            layout.addWidget(
                item
            )

            self.items.append(
                item
            )

            if text == "SQL Tools":

                setattr(
                    self,
                    "database_maintenance",
                    item,
                )

            elif text == "myDATA Manager":

                setattr(
                    self,
                    "mydata_sent",
                    item,
                )

            elif text == "Delete Pending Order":

                setattr(
                    self,
                    "support",
                    item,
                )

            elif text == "Empty Lock":

                setattr(
                    self,
                    "history",
                    item,
                )

            else:

                setattr(
                    self,
                    text.lower().replace(
                        " ",
                        "_",
                    ),
                    item,
                )

        layout.addStretch()

    # ==========================================================
    # TECHNICAL ACCESS
    # ==========================================================

    def update_technical_access(
        self,
        unlocked=None,
    ):

        if unlocked is None:

            unlocked = (
                TechnicalAccess.is_unlocked()
            )

        protected_items = [

            getattr(
                self,
                "history",
                None,
            ),

            getattr(
                self,
                "support",
                None,
            ),

            getattr(
                self,
                "database_maintenance",
                None,
            ),
        ]

        for item in protected_items:

            if item is None:
                continue

            item.setEnabled(
                unlocked
            )

            if unlocked:

                item.setToolTip(
                    ""
                )

            else:

                item.setToolTip(
                    "Technical access required"
                )

    # ==========================================================
    # ACTIVE ITEM
    # ==========================================================

    def set_active(
        self,
        current,
    ):

        if not current.isEnabled():

            return

        for item in self.items:

            item.setActive(
                item is current
            )