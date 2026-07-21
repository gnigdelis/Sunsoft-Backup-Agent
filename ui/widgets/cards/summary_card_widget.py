from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from ui.styles.theme import (
    CARD_HEIGHT,
    PANEL_BACKGROUND,
    PANEL_BORDER_COLOR,
    CARD_BORDER_SIZE,
    CARD_BORDER_RADIUS,
    GOLD_COLOR,
    WHITE_COLOR,
    SUCCESS_COLOR,
    SUBTITLE_FONT_SIZE,
    SMALL_FONT_SIZE,
)


class SummaryCardWidget(QFrame):

    def __init__(
        self,
        title: str,
        value: str,
        status: str = "",
    ):

        super().__init__()

        self.title = title
        self.value = value
        self.status = status

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):

        self.setFixedHeight(
            CARD_HEIGHT
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        layout.setSpacing(
            8
        )

        self.title_label = QLabel(
            self.title
        )

        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value_label = QLabel(
            self.value
        )

        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status_label = QLabel(
            self.status
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.title_label
        )

        layout.addStretch()

        layout.addWidget(
            self.value_label
        )

        layout.addStretch()

        layout.addWidget(
            self.status_label
        )

        self.setLayout(
            layout
        )

    def setup_styles(self):

        self.setStyleSheet(

            f"""

            SummaryCardWidget {{

                background-color: {PANEL_BACKGROUND};

                border: {CARD_BORDER_SIZE}px solid {PANEL_BORDER_COLOR};

                border-radius: {CARD_BORDER_RADIUS}px;

            }}

            """

        )

        self.title_label.setStyleSheet(

            f"""

            color: {GOLD_COLOR};

            font-size: {SUBTITLE_FONT_SIZE}pt;
            font-weight: bold;

            """

        )

        self.value_label.setStyleSheet(

            f"""

            color: {WHITE_COLOR};

            font-size: 24pt;
            font-weight: bold;

            """

        )

        self.status_label.setStyleSheet(

            f"""

            background-color: {SUCCESS_COLOR};

            color: {WHITE_COLOR};

            border-radius: 10px;

            padding: 5px;

            font-size: {SMALL_FONT_SIZE}pt;
            font-weight: bold;

            """

        )