from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
)

from ui.v2.widgets.cards.metric_card import MetricCard
from ui.v2.widgets.cards.last_backup_card import LastBackupCard
from ui.v2.widgets.progress.progress_card import ProgressCard


class SummarySection(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QGridLayout()

        layout.setHorizontalSpacing(15)
        layout.setVerticalSpacing(15)

        #
        # First Row
        #

        layout.addWidget(

            MetricCard(

                title="Customers",

                value="248",

                subtitle="Active installations",

                status="success",

            ),

            0,

            0,

        )

        layout.addWidget(

            MetricCard(

                title="Today's Backups",

                value="31",

                subtitle="Completed successfully",

                status="info",

            ),

            0,

            1,

        )

        layout.addWidget(

            MetricCard(

                title="Storage",

                value="1.82 TB",

                subtitle="Used",

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