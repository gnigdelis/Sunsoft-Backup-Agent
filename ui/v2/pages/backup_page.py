from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from ui.v2.styles.theme import Theme


class BackupPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Backup Manager")
        title.setFont(Theme.Typography.title())
        title.setStyleSheet(f"color:{Theme.Colors.TEXT};")

        layout.addWidget(title)
        layout.addStretch()