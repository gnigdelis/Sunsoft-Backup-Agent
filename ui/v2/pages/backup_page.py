from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.v2.backup.layouts.backup_layout import (
    BackupLayout,
)


class BackupPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            BackupLayout()
        )