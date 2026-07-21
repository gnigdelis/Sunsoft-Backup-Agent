from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)


class StatusRowWidget(QWidget):

    def __init__(
        self,
        title: str,
        status: str,
        duration: str,
    ):

        super().__init__()

        self.title = title
        self.status = status
        self.duration = duration

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
        # STATUS
        #

        self.status_label = QLabel(
            self.status
        )

        #
        # DURATION
        #

        self.duration_label = QLabel(
            self.duration
        )

        #
        # ADD LABELS
        #

        layout.addWidget(
            self.title_label,
            4,
        )

        layout.addWidget(
            self.status_label,
            1,
        )

        layout.addWidget(
            self.duration_label,
            1,
        )

        #
        # SET LAYOUT
        #

        self.setLayout(
            layout
        )

    def set_status(
        self,
        status: str,
    ):

        self.status_label.setText(
            status
        )

    def set_duration(
        self,
        duration: str,
    ):

        self.duration_label.setText(
            duration
        )