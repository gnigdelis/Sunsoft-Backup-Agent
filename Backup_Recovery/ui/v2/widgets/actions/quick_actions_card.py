from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.widgets.actions.quick_action_button import QuickActionButton
from ui.v2.styles.theme import Theme


class QuickActionsCard(BaseCard):

    def __init__(self):
        super().__init__(
            "Quick Actions",
            250,
        )

        self._create_buttons()

    def _create_buttons(self):

        actions = [
            ("Backup", "💾", "#e53935"),
            ("Upload", "☁", "#1e88e5"),
            ("Verify", "✓", "#43a047"),
            ("Restore", "↺", "#fb8c00"),
        ]

        for text, icon, color in actions:

            button = QuickActionButton(
                text=text,
                icon=icon,
                color=color,
            )

            self.add_widget(button)