from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from ui.styles.config import APPLICATION_VERSION

from ui.styles.theme import (
    PRIMARY_COLOR,
    WHITE_COLOR,
    SECONDARY_TEXT_COLOR,
)


class SidebarLogo(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(4)

        self.title_label = QLabel("Sunsoft")

        self.subtitle_label = QLabel(
            "Support Agent"
        )

        self.version_label = QLabel(
            f"Version {APPLICATION_VERSION}"
        )

        for label in (
            self.title_label,
            self.subtitle_label,
            self.version_label,
        ):

            label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

        self.title_label.setStyleSheet(

            f"""

            color:{PRIMARY_COLOR};
            font-size:22pt;
            font-weight:700;

            """

        )

        self.subtitle_label.setStyleSheet(

            f"""

            color:{WHITE_COLOR};
            font-size:12pt;
            font-weight:600;

            """

        )

        self.version_label.setStyleSheet(

            f"""

            color:{SECONDARY_TEXT_COLOR};
            font-size:9pt;

            """

        )

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.subtitle_label
        )

        layout.addSpacing(6)

        layout.addWidget(
            self.version_label
        )

        self.setLayout(layout)