from PySide6.QtWidgets import QLabel

from ui.v2.widgets.cards.base_card import BaseCard

from ui.v2.styles.theme import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class FilesCard(BaseCard):

    def __init__(self):

        super().__init__(

            title="Files",
            icon="📁"

        )

        self.build()

    def build(self):

        self.total_label = QLabel("12,248")

        self.total_label.setStyleSheet(

            f"""

            color:{TEXT_PRIMARY};

            font-size:22pt;

            font-weight:700;

            """

        )

        self.info_label = QLabel(
            "Total files backed up"
        )

        self.info_label.setStyleSheet(

            f"""

            color:{TEXT_SECONDARY};

            font-size:10pt;

            """

        )

        self.add_widget(self.total_label)
        self.add_widget(self.info_label)

        self.content_layout.addStretch()