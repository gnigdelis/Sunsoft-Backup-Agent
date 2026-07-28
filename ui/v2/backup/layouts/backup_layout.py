from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from ui.v2.styles.theme import Theme


class BackupLayout(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        layout.setSpacing(15)

        title = QLabel("Backup Manager")

        title.setFont(
            Theme.Typography.title()
        )

        title.setStyleSheet(
            f"color:{Theme.Colors.TEXT};"
        )

        layout.addWidget(title)

        layout.addStretch()