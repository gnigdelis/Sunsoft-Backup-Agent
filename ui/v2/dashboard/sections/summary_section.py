from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from core.discovery.system_discovery import SystemDiscovery

from ui.v2.widgets.cards.info_card import InfoCard
from ui.v2.widgets.cards.last_backup_card import LastBackupCard
from ui.v2.widgets.progress.progress_card import ProgressCard


class SummarySection(QWidget):

    def __init__(self):

        super().__init__()

        self.system = SystemDiscovery()

        self.system_info = self.system.discover()["data"]

        self.setup_ui()

    def setup_ui(self):

        layout = QGridLayout()

        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(15)

        #
        # Storage
        #

        total = float(
            self.system_info["total_disk"].replace(" GB", "")
        )

        free = float(
            self.system_info["free_disk"].replace(" GB", "")
        )

        used = round(total - free, 2)

        percent = round((used / total) * 100)

        #
        # First Row
        #

        layout.addWidget(

            InfoCard(

                title="Computer",

                lines=[

                    self.system_info["computer_name"],

                    self.system_info["windows_version"],

                    "Domain: (Coming Soon)",

                ],

                status="success",

            ),

            0,

            0,

        )

        layout.addWidget(

            InfoCard(

                title="Database",

                lines=[

                    "SQL Server",

                    "Connected",

                ],

                status="info",

            ),

            0,

            1,

        )

        layout.addWidget(

            InfoCard(

                title="Storage",

                lines=[

                    f"{used:.2f} GB Used",

                    f"{total:.2f} GB Total",

                    f"{percent}% Used",

                ],

                status="warning",

            ),

            0,

            2,

        )

        #
        # Second Row
        #

        layout.addWidget(

            LastBackupCard(),

            1,

            0,

            1,

            2,

        )

        layout.addWidget(

            ProgressCard(),

            1,

            2,

        )

        self.setLayout(layout)