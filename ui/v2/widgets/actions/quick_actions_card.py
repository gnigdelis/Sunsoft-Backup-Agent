from PySide6.QtCore import Signal

from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.widgets.actions.quick_action_button import QuickActionButton


class QuickActionsCard(BaseCard):

    backup_clicked = Signal()

    delete_mydata_clicked = Signal()

    upload_clicked = Signal()

    verify_clicked = Signal()

    def __init__(self):

        super().__init__(

            "Quick Actions",

            250,

        )

        self._create_buttons()

    def _create_buttons(self):

        actions = [

            (
                "Backup",
                "💾",
                "#E53935",
                self.backup_clicked,
            ),

            (
                "Delete MyDATA Response",
                "🧹",
                "#FB8C00",
                self.delete_mydata_clicked,
            ),

            (
                "Upload Backup",
                "☁",
                "#1E88E5",
                self.upload_clicked,
            ),

            (
                "Verify Backup",
                "✔",
                "#43A047",
                self.verify_clicked,
            ),

        ]

        for text, icon, color, signal in actions:

            button = QuickActionButton(

                text=text,

                icon=icon,

                color=color,

            )

            button.clicked.connect(

                signal.emit

            )

            self.add_widget(button)