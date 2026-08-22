from PySide6.QtCore import QThread
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


class DatabaseMaintenancePage(QWidget):

    def __init__(self):

        super().__init__()

        self.thread = None

        self.controller = None

        self.current_operation = None

        self.setup_ui()

        database_context.database_changed.connect(
            self.on_database_changed
        )

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )

        main_layout.setSpacing(
            12
        )

        #
        # Main Card
        #

        card = QFrame()

        card.setObjectName(
            "DatabaseMaintenanceCard"
        )

        card_layout = QVBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        card_layout.setSpacing(
            12
        )

        #
        # Title
        #

        title = QLabel(
            "Database Maintenance"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            """
        )

        card_layout.addWidget(
            title
        )

        #
        # Description
        #

        description = QLabel(
            "Εκτέλεση ανεξάρτητων εργασιών "
            "συντήρησης της βάσης δεδομένων."
        )

        description.setStyleSheet(
            """
            QLabel {
                color: #bdbdbd;
                font-size: 13px;
            }
            """
        )

        card_layout.addWidget(
            description
        )

        #
        # Buttons
        #

        buttons_layout = QHBoxLayout()

        buttons_layout.setSpacing(
            10
        )

        self.delete_button = QPushButton(
            "1. Delete MyDATA Response"
        )

        self.rebuild_button = QPushButton(
            "2. Rebuild Database"
        )

        self.shrink_button = QPushButton(
            "3. Shrink Database"
        )

        self.delete_button.setMinimumHeight(
            42
        )

        self.rebuild_button.setMinimumHeight(
            42
        )

        self.shrink_button.setMinimumHeight(
            42
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

        buttons_layout.addWidget(
            self.delete_button
        )

        buttons_layout.addWidget(
            self.rebuild_button
        )

        buttons_layout.addWidget(
            self.shrink_button
        )

        card_layout.addLayout(
            buttons_layout
        )

        #
        # Status
        #

        status_title = QLabel(
            "Status"
        )

        status_title.setStyleSheet(
            """
            QLabel {
                font-weight: bold;
            }
            """
        )

        card_layout.addWidget(
            status_title
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

        main_layout.addWidget(
            card
        )

        main_layout.addStretch()

    # ==========================================================
    # Database
    # ==========================================================

    def on_database_changed(
        self,
        database,
    ):

        if not database:

            return

        self.append_status(
            ""
        )

        self.append_status(
            f"Database selected: "
            f"{database.get('name', 'Unknown')}"
        )

        self.append_status(
            f"Server: "
            f"{database.get('server', 'Unknown')}"
        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def append_status(
        self,
        message,
    ):

        self.status.append(
            message
        )

    def set_buttons_enabled(
        self,
        enabled,
    ):

        self.delete_button.setEnabled(
            enabled
        )

        self.rebuild_button.setEnabled(
            enabled
        )

        self.shrink_button.setEnabled(
            enabled
        )

    def show_result(
        self,
        result,
    ):

        if result["success"]:

            self.append_status(
                f"✓ {result['step']} "
                f"completed successfully."
            )

            affected_rows = (
                result.get(
                    "affected_rows",
                    -1
                )
            )

            #
            # Only show affected rows when
            # the database operation actually
            # provides a valid row count.
            #

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

    def start_operation(
        self,
        operation,
        title,
    ):

        #
        # Safety check
        #

        if self.thread is not None:

            if self.thread.isRunning():

                return

        #
        # Database selection
        #

        database = (
            database_context.active()
        )

        if not database:

            self.append_status(
                ""
            )

            self.append_status(
                "✗ No database selected."
            )

            self.append_status(
                "Please select a database "
                "from the Dashboard."
            )

            return

        #
        # UI
        #

        self.set_buttons_enabled(
            False
        )

        self.current_operation = (
            operation
        )

        self.append_status(
            ""
        )

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

        #
        # Thread
        #

        self.thread = QThread(
            self
        )

        self.controller = (
            MaintenanceController(
                maintenance_service,
                self.thread,
                operation,
            )
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

    # ==========================================================
    # Started
    # ==========================================================

    def on_started(self):

        pass

    # ==========================================================
    # Finished
    # ==========================================================

    def on_finished(
        self,
        result,
    ):

        #
        # Remove "Running..."
        #

        self.show_result(
            result
        )

    # ==========================================================
    # Error
    # ==========================================================

    def on_error(
        self,
        message,
    ):

        self.append_status(
            f"✗ Error: {message}"
        )

    # ==========================================================
    # Thread Finished
    # ==========================================================

    def on_thread_finished(self):

        self.append_status(
            ""
        )

        self.append_status(
            "Ready."
        )

        self.set_buttons_enabled(
            True
        )

        self.current_operation = None

        self.controller = None

        self.thread = None

    # ==========================================================
    # Delete MyDATA Response
    # ==========================================================

    def delete_mydata_response(self):

        self.start_operation(
            "delete",
            "Delete MyDATA Response",
        )

    # ==========================================================
    # Rebuild Database
    # ==========================================================

    def rebuild_database(self):

        self.start_operation(
            "rebuild",
            "Rebuild Database",
        )

    # ==========================================================
    # Shrink Database
    # ==========================================================

    def shrink_database(self):

        self.start_operation(
            "shrink",
            "Shrink Database",
        )