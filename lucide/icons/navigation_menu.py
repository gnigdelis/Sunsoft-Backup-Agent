from PySide6.QtWidgets import QVBoxLayout, QWidget

from ui.v2.widgets.sidebar.navigation_item import NavigationItem


class NavigationMenu(QWidget):

    def __init__(self):

        super().__init__()

        self.items = []

        self.setup_ui()

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
                "lucide/icons/house.svg",
                "#e53935",
                True,
            ),

            (
                "Backup",
                "lucide/icons/upload.svg",
                "#8e24aa",
                False,
            ),

            (
                "Restore",
                "lucide/icons/rotate-ccw.svg",
                "#43a047",
                False,
            ),

            (
                "History",
                "lucide/icons/history.svg",
                "#1e88e5",
                False,
            ),

            (
                "Support",
                "lucide/icons/headset.svg",
                "#00acc1",
                False,
            ),

            (
                "MyData Sent",
                "lucide/icons/send.svg",
                "#757575",
                False,
            ),

            (
                "Settings",
                "lucide/icons/settings.svg",
                "#fb8c00",
                False,
            ),

            (
                "SQL Tools",
                "lucide/icons/database.svg",
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
                self.set_active(current)
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

            elif text == "MyData Sent":

                setattr(
                    self,
                    "mydata_sent",
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

    def set_active(
        self,
        current,
    ):

        for item in self.items:

            item.setActive(
                item is current
            )
