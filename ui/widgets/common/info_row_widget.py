from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
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

    def setup_ui(self):

        #
        # MAIN LAYOUT
        #

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            10
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
            3,
        )

        #
        # SET LAYOUT
        #

        self.setLayout(
            layout
        )

    def set_value(
        self,
        value: str,
    ):

        self.value_label.setText(
            value
        )