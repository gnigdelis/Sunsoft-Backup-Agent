from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.widgets.common.status_chip import StatusChip

from ui.v2.styles.theme import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class LastBackupCard(BaseCard):

    def __init__(self):

        super().__init__(

            title="Last Backup",
            icon="🗓"

        )

        self.build()

    def build(self):

        self.time_label = QLabel(
            "Today 17:42"
        )

        self.time_label.setStyleSheet(

            f"""

            color:{TEXT_PRIMARY};

            font-size:22pt;

            font-weight:700;

            """

        )

        self.date_label = QLabel(
            "26/07/2026 17:42:31"
        )

        self.date_label.setStyleSheet(

            f"""

            color:{TEXT_SECONDARY};

            font-size:10pt;

            """

        )

        self.status_chip = StatusChip(

            "SUCCESS",

            "success",

        )

        self.status_chip.setFixedWidth(
            90
        )

        self.status_chip.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.add_widget(
            self.time_label
        )

        self.add_widget(
            self.date_label
        )

        self.add_widget(
            self.status_chip
        )

        self.content_layout.addStretch()