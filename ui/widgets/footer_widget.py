from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from PySide6.QtCore import Qt

from ui.styles.config import (
    APPLICATION_NAME,
    APPLICATION_VERSION,
)

from ui.styles.theme import (
    PRIMARY_COLOR,
    WHITE_COLOR,
    SECONDARY_TEXT_COLOR,
)


class FooterWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setSpacing(
            5
        )

        self.application_label = QLabel(
            f"{APPLICATION_NAME} v{APPLICATION_VERSION}"
        )

        self.application_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.description_label = QLabel(
            "Professional Technical Support Utility"
        )

        self.description_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.copyright_label = QLabel(
            "© 2026 Sunsoft"
        )

        self.copyright_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.application_label
        )

        layout.addWidget(
            self.description_label
        )

        layout.addWidget(
            self.copyright_label
        )

        self.setLayout(
            layout
        )

    def setup_styles(self):

        self.application_label.setStyleSheet(

            f"""
            color: {PRIMARY_COLOR};
            font-size: 11pt;
            font-weight: bold;
            """

        )

        self.description_label.setStyleSheet(

            f"""
            color: {WHITE_COLOR};
            font-size: 9pt;
            """

        )

        self.copyright_label.setStyleSheet(

            f"""
            color: {SECONDARY_TEXT_COLOR};
            font-size: 8pt;
            """

        )