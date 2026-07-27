from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

from ui.v2.widgets.logs.live_activity_card import LiveActivityCard
from ui.v2.widgets.actions.quick_actions_card import QuickActionsCard


class OperationsSection(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(15)

        #
        # Left
        #

        self.live_activity = LiveActivityCard()

        #
        # Right
        #

        self.quick_actions = QuickActionsCard()

        #
        # Stretch
        #

        layout.addWidget(
            self.live_activity,
            3,
        )

        layout.addWidget(
            self.quick_actions,
            1,
        )

        self.setLayout(layout)