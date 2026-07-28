from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

from ui.v2.widgets.common.primary_button import PrimaryButton
from ui.v2.widgets.common.secondary_button import SecondaryButton


class BackupToolbar(QWidget):

    start_backup = Signal()
    browse_clicked = Signal()
    open_destination_clicked = Signal()

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.start_button = PrimaryButton(
            "Start Backup",
            "▶",
        )

        self.browse_button = SecondaryButton(
            "Browse",
            "📁",
        )

        self.open_button = SecondaryButton(
            "Open Folder",
            "📂",
        )

        layout.addWidget(self.start_button)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.open_button)
        layout.addStretch()

        self.start_button.clicked.connect(self.start_backup.emit)
        self.browse_button.clicked.connect(self.browse_clicked.emit)
        self.open_button.clicked.connect(self.open_destination_clicked.emit)