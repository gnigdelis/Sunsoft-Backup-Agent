from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from ui.styles.config import APPLICATION_VERSION

from ui.styles.theme import (
    SECONDARY_TEXT_COLOR,
    SUCCESS_COLOR,
    STATUS_READY,
)


class SidebarStatus(QWidget):

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

        self.status_title = QLabel(
            "ΚΑΤΑΣΤΑΣΗ"
        )

        self.status_label = QLabel(
            STATUS_READY
        )

        self.version_label = QLabel(
            f"v{APPLICATION_VERSION}"
        )

        for label in (
            self.status_title,
            self.status_label,
            self.version_label,
        ):

            label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

        self.status_title.setStyleSheet(

            f"""

            color:{SECONDARY_TEXT_COLOR};
            font-size:10pt;
            font-weight:600;

            """

        )

        self.status_label.setStyleSheet(

            f"""

            color:{SUCCESS_COLOR};
            font-size:12pt;
            font-weight:bold;

            """

        )

        self.version_label.setStyleSheet(

            f"""

            color:{SECONDARY_TEXT_COLOR};
            font-size:9pt;

            """

        )

        layout.addWidget(
            self.status_title
        )

        layout.addWidget(
            self.status_label
        )

        layout.addSpacing(6)

        layout.addWidget(
            self.version_label
        )

        self.setLayout(layout)

    def set_status(self, text: str, color: str):

        self.status_label.setText(text)

        self.status_label.setStyleSheet(

            f"""

            color:{color};
            font-size:12pt;
            font-weight:bold;

            """

        )