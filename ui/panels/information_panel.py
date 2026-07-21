from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

from ui.widgets.backup_details_widget import (
    BackupDetailsWidget,
)

from ui.widgets.system_info_widget import (
    SystemInfoWidget,
)

from ui.widgets.database_info_widget import (
    DatabaseInfoWidget,
)


class InformationPanel(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        #
        # MAIN LAYOUT
        #

        main_layout = QVBoxLayout()

        #
        # PANEL CONTAINER
        #

        panel_frame = QFrame()

        panel_layout = QHBoxLayout()

        panel_layout.setSpacing(20)

        panel_layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        #
        # LEFT COLUMN
        #

        left_layout = QVBoxLayout()

        left_layout.setSpacing(
            15
        )

        left_layout.addWidget(
            BackupDetailsWidget()
        )

        #
        # RIGHT COLUMN
        #

        right_layout = QVBoxLayout()

        right_layout.setSpacing(
            15
        )

        right_layout.addWidget(
            SystemInfoWidget()
        )

        right_layout.addWidget(
            DatabaseInfoWidget()
        )

        #
        # COLUMN SIZES
        #

        panel_layout.addLayout(
            left_layout,
            2,
        )

        panel_layout.addLayout(
            right_layout,
            1,
        )

        #
        # PANEL FRAME
        #

        panel_frame.setLayout(
            panel_layout
        )

        #
        # MAIN LAYOUT
        #

        main_layout.addWidget(
            panel_frame
        )

        self.setLayout(
            main_layout
        )