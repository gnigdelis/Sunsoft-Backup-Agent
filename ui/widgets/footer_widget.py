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
    SECONDARY_TEXT_COLOR,
    GOLD_COLOR,
    WHITE_COLOR,
)


class FooterWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):

        #
        # MAIN LAYOUT
        #

        layout = QVBoxLayout()
        layout.setSpacing(5)

        #
        # APPLICATION NAME
        #

        self.application_label = QLabel(
            f"{APPLICATION_NAME} v{APPLICATION_VERSION}"
        )

        self.application_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        #
        # DESCRIPTION
        #

        self.description_label = QLabel(
            "Internal Technical Support Utility"
        )

        self.description_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        #
        # COPYRIGHT
        #

        self.copyright_label = QLabel(
            "© 2026 Sunsoft Ltd."
        )

        self.copyright_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        #
        # ADD LABELS
        #

        layout.addWidget(
            self.application_label
        )

        layout.addWidget(
            self.description_label
        )

        layout.addWidget(
            self.copyright_label
        )

        #
        # SET LAYOUT
        #

        self.setLayout(layout)

    def setup_styles(self):

        #
        # APPLICATION NAME STYLE
        #

        self.application_label.setStyleSheet(

            f"""
            color: {GOLD_COLOR};
            font-size: 11pt;
            font-weight: bold;
            """

        )

        #
        # DESCRIPTION STYLE
        #

        self.description_label.setStyleSheet(

            f"""
            color: {WHITE_COLOR};
            font-size: 9pt;
            """

        )

        #
        # COPYRIGHT STYLE
        #

        self.copyright_label.setStyleSheet(

            f"""
            color: {SECONDARY_TEXT_COLOR};
            font-size: 8pt;
            """

        )