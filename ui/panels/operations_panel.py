from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

from ui.widgets.logs_widget import (
    LogsWidget,
)

from ui.widgets.action_buttons_widget import (
    ActionButtonsWidget,
)


class OperationsPanel(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QHBoxLayout()

        main_layout.setSpacing(15)

        #
        # LEFT COLUMN
        #

        left_layout = QVBoxLayout()

        self.logs_widget = (
            LogsWidget()
        )

        left_layout.addWidget(
            self.logs_widget
        )

        #
        # RIGHT COLUMN
        #

        right_layout = QVBoxLayout()

        self.action_buttons_widget = (
            ActionButtonsWidget()
        )

        right_layout.addWidget(
            self.action_buttons_widget
        )

        right_layout.addStretch()

        #
        # ADD COLUMNS
        #

        main_layout.addLayout(
            left_layout,
            5,
        )

        main_layout.addLayout(
            right_layout,
            2,
        )

        self.setLayout(
            main_layout
        )