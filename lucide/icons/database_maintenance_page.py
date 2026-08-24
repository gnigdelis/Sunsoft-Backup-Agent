from PySide6.QtCore import QThread, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
)

from core.controllers.maintenance_controller import (
    MaintenanceController,
)

from core.services.maintenance_service import (
    maintenance_service,
)

from core.database.database_context import (
    database_context,
)

from ui.v2.pages.database_maintenance.extra_lock_page import (
    ExtraLockPage,
)

from ui.v2.styles.icons import Icons
from ui.v2.widgets.common.svg_icon import SvgIcon


class DatabaseMaintenancePage(QWidget):

    def __init__(self):

        super().__init__()

        self.thread = None
        self.controller = None
        self.current_operation = None
        self.extra_lock_page = None

        self.setup_ui()

        database_context.database_changed.connect(
            self.on_database_changed
        )

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )

        main_layout.setSpacing(12)

        card = QFrame()
        card.setObjectName(
            "DatabaseMaintenanceCard"
        )

        card_layout = QVBoxLayout(card)

        card_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        card_layout.setSpacing(12)

        title = QLabel(
            "SQL Tools"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            """
        )

        card_layout.addWidget(title)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.delete_button = self.create_action_button(
            "Delete MyDATA Response",
            Icons.DELETE,
            "#e53935",
        )

        self.rebuild_button = self.create_action_button(
            "Rebuild Database",
            Icons.REBUILD,
            "#1e88e5",
        )

        self.shrink_button = self.create_action_button(
            "Shrink Database",
            Icons.DATABASE,
            "#fb8c00",
        )

        self.extra_lock_button = self.create_action_button(
            "Extra Lock",
            Icons.EXTRA_LOCK,
            "#8e24aa",
        )

        self.delete_button.clicked.connect(
            self.delete_mydata_response
        )

        self.rebuild_button.clicked.connect(
            self.rebuild_database
        )

        self.shrink_button.clicked.connect(
            self.shrink_database
        )

        self.extra_lock_button.clicked.connect(
            self.open_extra_lock
        )

        buttons_layout.addWidget(
            self.delete_button
        )

        buttons_layout.addWidget(
            self.rebuild_button
        )

        buttons_layout.addWidget(
            self.shrink_button
        )

        buttons_layout.addWidget(
            self.extra_lock_button
        )

        card_layout.addLayout(
            buttons_layout
        )

        self.extra_lock_page = ExtraLockPage(
            self
        )

        self.extra_lock_page.setMinimumHeight(
            480
        )

        self.extra_lock_page.hide()

        card_layout.addWidget(
            self.extra_lock_page,
            1,
        )

        self.status_title = QLabel(
            "Status"
        )

        self.status_title.setStyleSheet(
            """
            QLabel {
                font-weight: bold;
            }
            """
        )

        card_layout.addWidget(
            self.status_title
        )

        self.status = QTextEdit()

        self.status.setReadOnly(
            True
        )

        self.status.setMinimumHeight(
            180
        )

        self.status.setPlaceholderText(
            "Τα αποτελέσματα των εργασιών "
            "θα εμφανιστούν εδώ."
        )

        card_layout.addWidget(
            self.status
        )

        main_layout.addWidget(card)
        main_layout.addStretch()

        self.status_title.show()
        self.status.show()
        self.extra_lock_page.hide()

    # ==========================================================
    # SQL Tool Button
    # ==========================================================

    def create_action_button(
        self,
        text,
        icon_path,
        accent,
    ):

        button = QPushButton()

        button.setObjectName(
            "SqlToolButton"
        )

        button.setMinimumHeight(
            48
        )

        button.setCursor(
            Qt.PointingHandCursor
        )

        layout = QHBoxLayout(button)

        layout.setContentsMargins(
            10,
            6,
            12,
            6,
        )

        layout.setSpacing(9)

        icon_container = QFrame()
        icon_container.setFixedSize(
            34,
            34,
        )

        icon_container.setStyleSheet(
            f"""
            QFrame {{
                background:{accent};
                border-radius:8px;
            }}
            """
        )

        icon_layout = QHBoxLayout(
            icon_container
        )

        icon_layout.setContentsMargins(
            5,
            5,
            5,
            5,
        )

        icon_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        icon = SvgIcon(
            icon_path,
            size=22,
        )

        icon_layout.addWidget(icon)

        label = QLabel(
            text
        )

        label.setStyleSheet(
            """
            QLabel {
                background:transparent;
                color:#ffffff;
                font-size:10pt;
                font-weight:600;
            }
            """
        )

        layout.addWidget(
            icon_container
        )

        layout.addWidget(
            label
        )

        layout.addStretch()

        button.setStyleSheet(
            """
            QPushButton#SqlToolButton {
                background:#25262a;
                border:1px solid #3a3b40;
                border-radius:10px;
                text-align:left;
            }

            QPushButton#SqlToolButton:hover {
                background:#2d2f34;
                border:1px solid #55575e;
            }

            QPushButton#SqlToolButton:pressed {
                background:#202125;
            }

            QPushButton#SqlToolButton:disabled {
                background:#25262a;
                border:1px solid #333438;
            }
            """
        )

        return button

    # ==========================================================
    # Database
    # ==========================================================

    def on_database_changed(
        self,
        database,
    ):

        if not database:
            return

        self.append_status("")

        self.append_status(
            f"Database selected: "
            f"{database.get('name', 'Unknown')}"
        )

        self.append_status(
            f"Server: "
            f"{database.get('server', 'Unknown')}"
        )

    # ==========================================================
    # Extra Lock
    # ==========================================================

    def open_extra_lock(self):

        if not database_context.is_selected():

            self.append_status("")

            self.append_status(
                "Δεν έχει επιλεγεί βάση δεδομένων."
            )

            self.append_status(
                "Παρακαλώ επίλεξε βάση από το Dashboard."
            )

            return

        if self.extra_lock_page.isVisible():

            self.extra_lock_page.hide()

            self.status_title.show()
            self.status.show()

            self.extra_lock_button.setText(
                "Extra Lock"
            )

            return

        self.extra_lock_page.load_values()

        self.status_title.hide()
        self.status.hide()

        self.extra_lock_page.show()

        self.extra_lock_button.setText(
            "Close Extra Lock"
        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def append_status(
        self,
        message,
    ):

        self.status.append(message)

    def set_buttons_enabled(
        self,
        enabled,
    ):

        self.delete_button.setEnabled(enabled)
        self.rebuild_button.setEnabled(enabled)
        self.shrink_button.setEnabled(enabled)
        self.extra_lock_button.setEnabled(enabled)

    def show_result(
        self,
        result,
    ):

        if result["success"]:

            self.append_status(
                f"✓ {result['step']} "
                f"completed successfully."
            )

            affected_rows = result.get(
                "affected_rows",
                -1
            )

            if affected_rows >= 0:

                self.append_status(
                    f"Affected Rows: "
                    f"{affected_rows}"
                )

        else:

            self.append_status(
                f"✗ {result['step']} failed."
            )

            self.append_status(
                result["message"]
            )

    # ==========================================================
    # Operations
    # ==========================================================

    def start_operation(
        self,
        operation,
        title,
    ):

        if self.thread is not None:

            if self.thread.isRunning():
                return

        database = (
            database_context.active()
        )

        if not database:

            self.append_status("")

            self.append_status(
                "Δεν έχει επιλεγεί βάση δεδομένων."
            )

            self.append_status(
                "Παρακαλώ επίλεξε βάση από το Dashboard."
            )

            return

        self.set_buttons_enabled(False)

        self.current_operation = operation

        self.append_status("")

        self.append_status(
            f"▶ {title}"
        )

        self.append_status(
            f"Database: "
            f"{database.get('name', 'Unknown')}"
        )

        self.append_status(
            "Running..."
        )

        self.thread = QThread(self)

        self.controller = MaintenanceController(
            maintenance_service,
            self.thread,
            operation,
        )

        self.controller.started.connect(
            self.on_started
        )

        self.controller.finished.connect(
            self.on_finished
        )

        self.controller.error.connect(
            self.on_error
        )

        self.thread.finished.connect(
            self.on_thread_finished
        )

        self.controller.start()

    def on_started(self):
        pass

    def on_finished(
        self,
        result,
    ):

        self.show_result(result)

    def on_error(
        self,
        message,
    ):

        self.append_status(
            f"✗ Error: {message}"
        )

    def on_thread_finished(self):

        self.append_status("")

        self.append_status(
            "Ready."
        )

        self.set_buttons_enabled(True)

        self.current_operation = None
        self.controller = None
        self.thread = None

    def delete_mydata_response(self):

        self.start_operation(
            "delete",
            "Delete MyDATA Response",
        )

    def rebuild_database(self):

        self.start_operation(
            "rebuild",
            "Rebuild Database",
        )

    def shrink_database(self):

        self.start_operation(
            "shrink",
            "Shrink Database",
        )
