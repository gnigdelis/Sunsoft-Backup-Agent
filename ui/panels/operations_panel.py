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

        main_layout = QHBoxLayout()

        #
        # LEFT COLUMN
        #

        left_layout = QVBoxLayout()

        left_layout.addWidget(
            LogsWidget()
        )

        #
        # RIGHT COLUMN
        #

        right_layout = QVBoxLayout()

        right_layout.addWidget(
            ActionButtonsWidget()
        )

        #
        # ADD COLUMNS
        #

        main_layout.addLayout(
            left_layout
        )

        main_layout.addLayout(
            right_layout
        )

        self.setLayout(
            main_layout
        )