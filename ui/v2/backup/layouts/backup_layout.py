from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
)

from core.controllers.backup_controller import BackupController

from ui.v2.styles.theme import Theme

from ui.v2.backup.widgets.backup_toolbar import BackupToolbar
from ui.v2.widgets.backup.progress_card import ProgressCard
from ui.v2.widgets.backup.customer_card import CustomerCard
from ui.v2.widgets.backup.statistics_card import StatisticsCard
from ui.v2.widgets.logs.live_activity_card import LiveActivityCard


class BackupLayout(QWidget):

    def __init__(self):

        super().__init__()

        self.backup_controller = BackupController()

        self.setup_ui()

    def setup_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        #
        # Header
        #

        header = QHBoxLayout()

        title = QLabel("Backup Manager")
        title.setFont(
            Theme.Typography.title()
        )

        title.setStyleSheet(
            f"color:{Theme.Colors.TEXT};"
        )

        self.status = QLabel("🟢 Ready")

        self.status.setStyleSheet(
            f"color:{Theme.Colors.SUCCESS}; font-size:11pt;"
        )

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.status)

        #
        # Widgets
        #

        self.toolbar = BackupToolbar()

        self.progress_card = ProgressCard()

        self.customer_card = CustomerCard()

        self.activity_card = LiveActivityCard()

        self.statistics_card = StatisticsCard()

        #
        # Middle Area
        #

        middle = QHBoxLayout()

        middle.setSpacing(20)

        middle.addWidget(
            self.customer_card,
            1,
        )

        middle.addWidget(
            self.activity_card,
            2,
        )

        #
        # Build Layout
        #

        root.addLayout(header)

        root.addWidget(self.toolbar)

        root.addWidget(self.progress_card)

        root.addLayout(middle)

        root.addWidget(self.statistics_card)

        root.addStretch()

        #
        # Backup Events
        #

        self.backup_controller.progress_changed.connect(
            self.progress_card.update_progress
        )

        self.backup_controller.finished.connect(
            self.progress_card.reset
        )