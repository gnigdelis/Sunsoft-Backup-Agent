from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)

from ui.styles.theme import (
    WHITE_COLOR,
    SECONDARY_TEXT_COLOR,
)


class InfoRowWidget(QWidget):

    def __init__(
        self,
        title: str,
        value: str,
    ):

        super().__init__()

        self.title = title
        self.value = value

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):

        #
        # MAIN LAYOUT
        #

        layout = QHBoxLayout()

        layout.setContentsMargins(
            5,
            5,
            5,
            5,
        )

        layout.setSpacing(
            15
        )

        #
        # TITLE
        #

        self.title_label = QLabel(
            self.title
        )

        #
        # VALUE
        #

        self.value_label = QLabel(
            self.value
        )

        #
        # ADD LABELS
        #

        layout.addWidget(
            self.title_label,
            2,
        )

        layout.addWidget(
            self.value_label,
            1,
        )

        #
        # SET LAYOUT
        #

        self.setLayout(
            layout
        )

    def setup_styles(self):

        self.title_label.setStyleSheet(

            f"""

            color: {WHITE_COLOR};

            font-size: 10pt;
            font-weight: bold;

            """

        )

        self.value_label.setStyleSheet(

            f"""

            color: {SECONDARY_TEXT_COLOR};

            font-size: 10pt;

            """

        )

    def set_value(
        self,
        value: str,
    ):

        self.value = value

        self.value_label.setText(
            value
        )