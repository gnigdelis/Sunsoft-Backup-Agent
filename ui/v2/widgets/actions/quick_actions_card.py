from PySide6.QtCore import Signal

from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.widgets.actions.quick_action_button import QuickActionButton


class QuickActionsCard(BaseCard):

    backup_clicked = Signal()
    upload_clicked = Signal()
    verify_clicked = Signal()
    rebuild_clicked = Signal()
    delete_mydata_clicked = Signal()

    def __init__(self):
        super().__init__(
            "Quick Actions",
            250,
        )

        self._create_buttons()

    def _create_buttons(self):

        actions = [
            ("Backup", "💾", "#e53935", self.backup_clicked),
            ("Upload", "☁", "#1e88e5", self.upload_clicked),
            ("Verify", "✓", "#43a047", self.verify_clicked),
            ("Rebuild", "🛠", "#fb8c00", self.rebuild_clicked),
            ("Delete MyData", "🗑", "#8e24aa", self.delete_mydata_clicked),
        ]

        for text, icon, color, signal in actions:

            button = QuickActionButton(
                text=text,
                icon=icon,
                color=color,
            )

            button.clicked.connect(signal.emit)

            self.add_widget(button)