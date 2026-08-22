from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)

from ui.v2.styles.theme import Theme


class DatabaseSelector(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.selected_udl = None

        self.setWindowTitle(
            "Select Database"
        )

        self.setMinimumSize(
            650,
            420
        )

        self.setup_ui()

        self.load_databases()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(12)

        title = QLabel(
            "Select Database"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 15pt;
                font-weight: 700;
            }
            """
        )

        description = QLabel(
            "Select the UDL file and database you want to work with."
        )

        description.setStyleSheet(
            """
            QLabel {
                color: #aaaaaa;
                font-size: 10pt;
            }
            """
        )

        self.list = QListWidget()

        self.list.setStyleSheet(
            f"""
            QListWidget {{
                background: {Theme.Colors.SURFACE};
                border: 1px solid {Theme.Colors.BORDER};
                border-radius: 8px;
                padding: 6px;
            }}

            QListWidget::item {{
                padding: 10px;
                border-radius: 6px;
            }}

            QListWidget::item:selected {{
                background: {Theme.Colors.PRIMARY};
                color: white;
            }}
            """
        )

        buttons = QHBoxLayout()

        buttons.addStretch()

        cancel = QPushButton(
            "Cancel"
        )

        cancel.clicked.connect(
            self.reject
        )

        connect = QPushButton(
            "Connect"
        )

        connect.setCursor(
            Qt.PointingHandCursor
        )

        connect.setStyleSheet(
            f"""
            QPushButton {{
                background: {Theme.Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 9px 24px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                background: #ff4b4b;
            }}
            """
        )

        connect.clicked.connect(
            self.select_database
        )

        buttons.addWidget(
            cancel
        )

        buttons.addWidget(
            connect
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            description
        )

        layout.addWidget(
            self.list,
            1
        )

        layout.addLayout(
            buttons
        )

    def load_databases(self):

        from core.database.database_context import (
            database_context
        )

        databases = (
            database_context.available_databases()
        )

        for database in databases:

            text = (
                f"Database: {database['name'] or '-'}\n"
                f"Server: {database['server'] or '-'}\n"
                f"UDL: {database['path']}"
            )

            item = QListWidgetItem(
                text
            )

            item.setData(
                Qt.UserRole,
                database["path"]
            )

            self.list.addItem(
                item
            )

        if self.list.count() > 0:

            self.list.setCurrentRow(0)

    def select_database(self):

        item = self.list.currentItem()

        if not item:
            return

        self.selected_udl = item.data(
            Qt.UserRole
        )

        self.accept()