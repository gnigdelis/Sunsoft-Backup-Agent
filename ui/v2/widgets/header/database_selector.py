from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
)

from ui.v2.styles.theme import Theme
from core.database.database_context import database_context


class DatabaseSelector(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_udl = None
        self.disconnect_requested = False

        self.setWindowTitle(
            "Select Database"
        )

        self.setMinimumSize(
            720,
            500
        )

        self.resize(
            720,
            500
        )

        self.setup_ui()
        self.load_databases()

    def setup_ui(self):

        self.setStyleSheet(
            f"""
            QDialog {{
                background: #202125;
                color: #ffffff;
            }}

            QLabel {{
                background: transparent;
            }}

            QListWidget {{
                background: #24262b;
                border: 1px solid #373a40;
                border-radius: 12px;
                padding: 8px;
                outline: none;
            }}

            QListWidget::item {{
                background: #292b30;
                color: #ffffff;
                border: 1px solid #373a40;
                border-radius: 10px;
                padding: 12px 14px;
                margin: 4px 2px;
            }}

            QListWidget::item:hover {{
                background: #2f3238;
                border: 1px solid #4b4f57;
            }}

            QListWidget::item:selected {{
                background: #303339;
                color: #ffffff;
                border: 1px solid {Theme.Colors.PRIMARY};
            }}

            QListWidget::item:selected:active {{
                background: #303339;
                color: #ffffff;
                border: 1px solid {Theme.Colors.PRIMARY};
            }}

            QScrollBar:vertical {{
                background: transparent;
                width: 8px;
                margin: 8px 2px 8px 2px;
            }}

            QScrollBar::handle:vertical {{
                background: #484c54;
                border-radius: 4px;
                min-height: 30px;
            }}

            QScrollBar::handle:vertical:hover {{
                background: #5b606a;
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            /* =========================================
               ACTION BUTTONS
               ========================================= */

            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 0px;
                min-height: 40px;
                padding: 0px 12px;
                color: #d8dbe0;
                font-size: 11pt;
                font-weight: 600;
            }}

            QPushButton:hover {{
                background: #292b30;
                color: #ffffff;
            }}

            QPushButton:pressed {{
                background: #303238;
            }}

            QPushButton#connectButton {{
                color: #4CAF50;
                font-weight: 700;
            }}

            QPushButton#connectButton:hover {{
                color: #66BB6A;
                background: #242b25;
            }}

            QPushButton#connectButton:disabled {{
                color: #666b73;
                background: transparent;
            }}

            QPushButton#disconnectButton {{
                color: #ff5c5c;
                font-weight: 700;
            }}

            QPushButton#disconnectButton:hover {{
                background: #2d2729;
                color: #ff7777;
            }}

            QPushButton#cancelButton {{
                color: #d8dbe0;
            }}

            QPushButton#cancelButton:hover {{
                color: #ffffff;
            }}
            """
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            24,
            22,
            24,
            20
        )

        layout.setSpacing(
            14
        )

        # =========================================
        # HEADER
        # =========================================

        header = QHBoxLayout()

        header.setSpacing(
            12
        )

        icon = QLabel(
            "▣"
        )

        icon.setFixedSize(
            42,
            42
        )

        icon.setAlignment(
            Qt.AlignCenter
        )

        icon.setStyleSheet(
            f"""
            QLabel {{
                background: #2b2d32;
                color: {Theme.Colors.PRIMARY};
                border: 1px solid #41444b;
                border-radius: 10px;
                font-size: 18pt;
                font-weight: 700;
            }}
            """
        )

        title_block = QVBoxLayout()

        title_block.setSpacing(
            2
        )

        title = QLabel(
            "Select Database"
        )

        title.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 15pt;
                font-weight: 700;
            }
            """
        )

        description = QLabel(
            "Choose the database you want to work with."
        )

        description.setStyleSheet(
            """
            QLabel {
                color: #9297a0;
                font-size: 9.5pt;
            }
            """
        )

        title_block.addWidget(
            title
        )

        title_block.addWidget(
            description
        )

        header.addWidget(
            icon
        )

        header.addLayout(
            title_block
        )

        header.addStretch()

        layout.addLayout(
            header
        )

        # =========================================
        # SECTION
        # =========================================

        section = QLabel(
            "AVAILABLE DATABASES"
        )

        section.setStyleSheet(
            """
            QLabel {
                color: #747a84;
                font-size: 8.5pt;
                font-weight: 700;
                letter-spacing: 1px;
            }
            """
        )

        layout.addWidget(
            section
        )

        # =========================================
        # DATABASE LIST
        # =========================================

        self.list = QListWidget()

        self.list.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.list.setFocusPolicy(
            Qt.NoFocus
        )

        self.list.setSpacing(
            2
        )

        self.list.itemDoubleClicked.connect(
            self.select_database
        )

        self.list.currentItemChanged.connect(
            self._update_connect_button
        )

        layout.addWidget(
            self.list,
            1
        )

        # =========================================
        # FOOTER
        # =========================================

        footer = QHBoxLayout()

        footer.setSpacing(
            4
        )

        self.status_label = QLabel(
            "Select a database to continue."
        )

        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #777d87;
                font-size: 8.5pt;
            }
            """
        )

        footer.addWidget(
            self.status_label
        )

        footer.addStretch()

        # =========================================
        # CONNECT
        # =========================================

        connect = QPushButton(
            "Connect"
        )

        connect.setObjectName(
            "connectButton"
        )

        connect.setCursor(
            Qt.PointingHandCursor
        )

        connect.setMinimumWidth(
            82
        )

        connect.setEnabled(
            False
        )

        connect.clicked.connect(
            self.select_database
        )

        self.connect_button = connect

        # =========================================
        # DISCONNECT
        # =========================================

        disconnect = QPushButton(
            "Disconnect"
        )

        disconnect.setObjectName(
            "disconnectButton"
        )

        disconnect.setCursor(
            Qt.PointingHandCursor
        )

        disconnect.setMinimumWidth(
            92
        )

        disconnect.clicked.connect(
            self.disconnect_database
        )

        self.disconnect_button = disconnect

        # =========================================
        # CANCEL
        # =========================================

        cancel = QPushButton(
            "Cancel"
        )

        cancel.setObjectName(
            "cancelButton"
        )

        cancel.setCursor(
            Qt.PointingHandCursor
        )

        cancel.setMinimumWidth(
            72
        )

        cancel.clicked.connect(
            self.reject
        )

        # =========================================
        # ORDER
        #
        # Connect -> Disconnect -> Cancel
        # =========================================

        footer.addWidget(
            connect
        )

        footer.addWidget(
            disconnect
        )

        footer.addWidget(
            cancel
        )

        layout.addLayout(
            footer
        )

    # ==========================================================
    # LOAD DATABASES
    # ==========================================================

    def load_databases(self):

        databases = (
            database_context.available_databases()
        )

        for database in databases:

            name = (
                database.get("name")
                or "Unnamed Database"
            )

            server = (
                database.get("server")
                or "Unknown Server"
            )

            path = (
                database.get("path")
                or "-"
            )

            text = (
                f"Database: {name}\n"
                f"Server: {server}\n"
                f"UDL: {path}"
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

        count = self.list.count()

        if count > 0:

            self.list.setCurrentRow(
                0
            )

            self.status_label.setText(
                f"{count} database"
                f"{'' if count == 1 else 's'} available."
            )

        else:

            self.status_label.setText(
                "No databases were found."
            )

    # ==========================================================
    # UPDATE CONNECT BUTTON
    # ==========================================================

    def _update_connect_button(
        self,
        current,
        previous,
    ):

        enabled = (
            current is not None
            and bool(
                current.data(
                    Qt.UserRole
                )
            )
        )

        self.connect_button.setEnabled(
            enabled
        )

        if enabled:

            self.status_label.setText(
                "Database selected. "
                "Press Connect to continue."
            )

        else:

            self.status_label.setText(
                "Select a database to continue."
            )

    # ==========================================================
    # CONNECT
    # ==========================================================

    def select_database(self):

        item = self.list.currentItem()

        if not item:
            return

        udl_path = item.data(
            Qt.UserRole
        )

        if not udl_path:
            return

        self.selected_udl = udl_path
        self.disconnect_requested = False

        self.accept()

    # ==========================================================
    # DISCONNECT
    # ==========================================================

    def disconnect_database(self):

        self.selected_udl = None
        self.disconnect_requested = True

        # Clear the currently selected database.
        database_context._active_udl = None

        # Notify every UI component listening for
        # database changes.
        database_context.database_changed.emit(
            None
        )

        self.reject()