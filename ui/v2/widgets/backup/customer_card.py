from PySide6.QtWidgets import (
    QLabel,
    QGridLayout,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.cards.base_card import BaseCard


class CustomerCard(BaseCard):

    def __init__(self):
        super().__init__(
            title="Customer Information",
            minimum_height=220,
        )

        self.build()

    def build(self):

        self.content_layout.setSpacing(
            11
        )

        # ======================================================
        # PURPLE ACCENT
        # ======================================================

        accent = QLabel()

        accent.setFixedHeight(
            3
        )

        accent.setStyleSheet(
            """
            QLabel {
                background: #9C27B0;
                border: none;
                border-radius: 1px;
            }
            """
        )

        self.content_layout.insertWidget(
            0,
            accent
        )

        # ======================================================
        # INFORMATION
        # ======================================================

        self.customer = self._value()
        self.sql_server = self._value()
        self.destination = self._value()
        self.cloud = self._value()
        self.last_backup = self._value()

        grid = QGridLayout()

        grid.setContentsMargins(
            0,
            4,
            0,
            0
        )

        grid.setHorizontalSpacing(
            22
        )

        grid.setVerticalSpacing(
            11
        )

        rows = [
            ("Customer", self.customer),
            ("SQL Server", self.sql_server),
            ("Destination", self.destination),
            ("Cloud", self.cloud),
            ("Last Backup", self.last_backup),
        ]

        for row, (
            title,
            value
        ) in enumerate(rows):

            label = QLabel(
                title
            )

            label.setStyleSheet(
                f"""
                QLabel {{
                    color:{Theme.Colors.TEXT_SECONDARY};
                    font-size:8.5pt;
                    font-weight:600;
                }}
                """
            )

            grid.addWidget(
                label,
                row,
                0
            )

            grid.addWidget(
                value,
                row,
                1
            )

        self.content_layout.addLayout(
            grid
        )

        self.content_layout.addStretch()

    def _value(self):

        label = QLabel(
            "-"
        )

        label.setWordWrap(
            True
        )

        label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:9pt;
                font-weight:600;
            }}
            """
        )

        return label

    def set_customer(
        self,
        customer: str,
        sql_server: str,
        destination: str,
        cloud: str,
        last_backup: str,
    ):

        self.customer.setText(
            customer
        )

        self.sql_server.setText(
            sql_server
        )

        self.destination.setText(
            destination
        )

        self.cloud.setText(
            cloud
        )

        self.last_backup.setText(
            last_backup
        )