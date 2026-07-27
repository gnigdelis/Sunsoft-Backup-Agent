from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout

from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.styles.theme import Theme


class InfoRow(QFrame):

    def __init__(self, title: str, value: str):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 6)
        layout.setSpacing(2)

        lbl_title = QLabel(title)
        lbl_value = QLabel(value)

        lbl_title.setStyleSheet(f"""
            QLabel {{
                color: {Theme.Colors.TEXT_DISABLED};
                font-size: 9pt;
                background: transparent;
            }}
        """)

        lbl_value.setStyleSheet(f"""
            QLabel {{
                color: {Theme.Colors.TEXT};
                font-size: 11pt;
                font-weight: 600;
                background: transparent;
            }}
        """)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)


class SystemInfoCard(BaseCard):

    def __init__(self):
        super().__init__(
            "System Information",
            300,
        )

        self.add_widget(
            InfoRow(
                "Database",
                "Connected",
            )
        )

        self.add_widget(
            InfoRow(
                "Backup Engine",
                "Running",
            )
        )

        self.add_widget(
            InfoRow(
                "Last Backup",
                "Today 13:42",
            )
        )

        self.add_widget(
            InfoRow(
                "Version",
                "v2.0.0",
            )
        )