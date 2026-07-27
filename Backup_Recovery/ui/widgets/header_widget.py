from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from PySide6.QtCore import Qt

from ui.styles.config import (
    APPLICATION_VERSION,
)

from ui.styles.theme import (
    PRIMARY_COLOR,
    WHITE_COLOR,
    SECONDARY_TEXT_COLOR,
)


class HeaderWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):

        main_layout = QHBoxLayout()

        #
        # LEFT SIDE
        #

        left_layout = QVBoxLayout()

        self.title_label = QLabel(
            "Sunsoft Support Agent"
        )

        self.subtitle_label = QLabel(
            "Professional Technical Support Utility\nfor Sunsoft Systems"
        )

        left_layout.addWidget(
            self.title_label
        )

        left_layout.addWidget(
            self.subtitle_label
        )

        #
        # RIGHT SIDE
        #

        right_layout = QVBoxLayout()

        self.version_label = QLabel(
            f"Version {APPLICATION_VERSION}"
        )

        self.version_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        right_layout.addStretch()

        right_layout.addWidget(
            self.version_label
        )

        #
        # ADD LAYOUTS
        #

        main_layout.addLayout(
            left_layout,
            4,
        )

        main_layout.addLayout(
            right_layout,
            1,
        )

        self.setLayout(
            main_layout
        )

    def setup_styles(self):

        self.title_label.setStyleSheet(

            f"""
            color: {PRIMARY_COLOR};
            font-size: 24pt;
            font-weight: bold;
            """

        )

        self.subtitle_label.setStyleSheet(

            f"""
            color: {WHITE_COLOR};
            font-size: 11pt;
            """

        )

        self.version_label.setStyleSheet(

            f"""
            color: {SECONDARY_TEXT_COLOR};
            font-size: 10pt;
            """

        )