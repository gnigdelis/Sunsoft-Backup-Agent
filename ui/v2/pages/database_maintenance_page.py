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

from ui.v2.styles.icons import Icons
from ui.v2.widgets.common.svg_icon import SvgIcon


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
            20,
            18,
            20,
            22,
        )

        main_layout.setSpacing(
            14
        )

        # ======================================================
        # PAGE HEADER
        # ======================================================

        header = QVBoxLayout()

        header.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        header.setSpacing(
            2
        )

        title = QLabel(
            "SQL Tools"
        )

        title.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#F5F7FA;
                font-size:26pt;
                font-weight:700;
                padding:0;
                margin:0;
            }
            """
        )

        subtitle = QLabel(
            "Database maintenance and recovery tools"
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#98A3B3;
                font-size:10.5pt;
                font-weight:400;
                padding:0;
                margin:0;
            }
            """
        )

        header.addWidget(
            title
        )

        header.addWidget(
            subtitle
        )

        main_layout.addLayout(
            header
        )

        # ======================================================
        # SQL ACTIONS
        # ======================================================

        actions_title = QLabel(
            "SQL Actions"
        )

        actions_title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:10pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        main_layout.addWidget(
            actions_title
        )

        actions_layout = QHBoxLayout()

        actions_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        actions_layout.setSpacing(
            24
        )

        self.delete_button = (
            self.create_action_button(
                "▶  Delete MyDATA Response",
                Icons.DELETE,
                "#E53935",
            )
        )

        self.rebuild_button = (
            self.create_action_button(
                "▶  Rebuild Database",
                Icons.REBUILD,
                "#29A8FF",
            )
        )

        self.shrink_button = (
            self.create_action_button(
                "▶  Shrink Database",
                Icons.DATABASE,
                "#FF9800",
            )
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

        actions_layout.addWidget(
            self.delete_button,
            1
        )

        actions_layout.addWidget(
            self.rebuild_button,
            1
        )

        actions_layout.addWidget(
            self.shrink_button,
            1
        )

        actions_layout.addStretch()

        main_layout.addLayout(
            actions_layout
        )

        # ======================================================
        # SQL OPERATION
        # ======================================================

        operation_card = QFrame()

        operation_card.setObjectName(
            "SqlOperationCard"
        )

        operation_card.setStyleSheet(
            """
            QFrame#SqlOperationCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        operation_layout = QVBoxLayout(
            operation_card
        )

        operation_layout.setContentsMargins(
            16,
            14,
            16,
            16
        )

        operation_layout.setSpacing(
            10
        )

        operation_title = QLabel(
            "SQL Operation"
        )

        operation_title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:11pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        operation_layout.addWidget(
            operation_title
        )

        operation_accent = QLabel()

        operation_accent.setFixedHeight(
            3
        )

        operation_accent.setStyleSheet(
            """
            QLabel {
                background:#AB47BC;
                border:none;
            }
            """
        )

        operation_layout.addWidget(
            operation_accent
        )

        operation_header = QHBoxLayout()

        operation_label = QLabel(
            "Current Operation"
        )

        operation_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                background:transparent;
                border:none;
            }
            """
        )

        self.operation_value = QLabel(
            "Waiting..."
        )

        self.operation_value.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.operation_value.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:10pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        operation_header.addWidget(
            operation_label
        )

        operation_header.addStretch()

        operation_header.addWidget(
            self.operation_value
        )

        operation_layout.addLayout(
            operation_header
        )

        operation_state_row = QHBoxLayout()

        state_label = QLabel(
            "State"
        )

        state_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                background:transparent;
                border:none;
            }
            """
        )

        self.operation_state_value = QLabel(
            "Ready"
        )

        self.operation_state_value.setStyleSheet(
            """
            QLabel {
                color:#53C653;
                font-size:9pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        operation_state_row.addWidget(
            state_label
        )

        operation_state_row.addStretch()

        operation_state_row.addWidget(
            self.operation_state_value
        )

        operation_layout.addLayout(
            operation_state_row
        )

        self.operation_task = QLabel(
            "SQL maintenance operation is ready."
        )

        self.operation_task.setStyleSheet(
            """
            QLabel {
                color:#D9DCE2;
                font-size:10pt;
                font-weight:600;
                background:transparent;
                border:none;
            }
            """
        )

        operation_layout.addWidget(
            self.operation_task
        )

        main_layout.addWidget(
            operation_card
        )

        # ======================================================
        # DATABASE / LIVE LOGS
        # ======================================================

        operation_area = QWidget()

        operation_area_layout = QHBoxLayout(
            operation_area
        )

        operation_area_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        operation_area_layout.setSpacing(
            14
        )

        # ======================================================
        # DATABASE INFORMATION
        # ======================================================

        database_card = QFrame()

        database_card.setObjectName(
            "SqlDatabaseCard"
        )

        database_card.setStyleSheet(
            """
            QFrame#SqlDatabaseCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        database_layout = QVBoxLayout(
            database_card
        )

        database_layout.setContentsMargins(
            16,
            14,
            16,
            16
        )

        database_layout.setSpacing(
            10
        )

        database_title = QLabel(
            "Database Information"
        )

        database_title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:11pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        database_layout.addWidget(
            database_title
        )

        database_accent = QLabel()

        database_accent.setFixedHeight(
            3
        )

        database_accent.setStyleSheet(
            """
            QLabel {
                background:#AB47BC;
                border:none;
            }
            """
        )

        database_layout.addWidget(
            database_accent
        )

        database_caption = QLabel(
            "Database"
        )

        database_caption.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                background:transparent;
                border:none;
            }
            """
        )

        database_layout.addWidget(
            database_caption
        )

        self.database_name_value = QLabel(
            "Not selected"
        )

        self.database_name_value.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:10pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        database_layout.addWidget(
            self.database_name_value
        )

        server_caption = QLabel(
            "SQL Server"
        )

        server_caption.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                background:transparent;
                border:none;
            }
            """
        )

        database_layout.addWidget(
            server_caption
        )

        self.database_server_value = QLabel(
            "-"
        )

        self.database_server_value.setStyleSheet(
            """
            QLabel {
                color:#B7BBC3;
                font-size:9pt;
                background:transparent;
                border:none;
            }
            """
        )

        database_layout.addWidget(
            self.database_server_value
        )

        status_caption = QLabel(
            "Status"
        )

        status_caption.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                background:transparent;
                border:none;
            }
            """
        )

        database_layout.addWidget(
            status_caption
        )

        self.database_state_value = QLabel(
            "Waiting..."
        )

        self.database_state_value.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        database_layout.addWidget(
            self.database_state_value
        )

        database_layout.addStretch()

        operation_area_layout.addWidget(
            database_card,
            3
        )

        # ======================================================
        # LIVE LOGS
        # ======================================================

        logs_card = QFrame()

        logs_card.setObjectName(
            "SqlLogsCard"
        )

        logs_card.setStyleSheet(
            """
            QFrame#SqlLogsCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        logs_layout = QVBoxLayout(
            logs_card
        )

        logs_layout.setContentsMargins(
            16,
            14,
            16,
            16
        )

        logs_layout.setSpacing(
            10
        )

        logs_title = QLabel(
            "Live Logs"
        )

        logs_title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:11pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        logs_layout.addWidget(
            logs_title
        )

        logs_accent = QLabel()

        logs_accent.setFixedHeight(
            3
        )

        logs_accent.setStyleSheet(
            """
            QLabel {
                background:#29A8FF;
                border:none;
            }
            """
        )

        logs_layout.addWidget(
            logs_accent
        )

        self.status = QTextEdit()

        self.status.setReadOnly(
            True
        )

        self.status.setPlaceholderText(
            "The results of database operations will appear here."
        )

        self.status.setStyleSheet(
            """
            QTextEdit {
                background:#202226;
                color:#D9DCE2;
                border:none;
                padding:10px;
                font-size:9pt;
            }

            QScrollBar:vertical {
                background:#202226;
                width:10px;
                margin:0;
            }

            QScrollBar::handle:vertical {
                background:#3B3F46;
                min-height:30px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height:0;
            }
            """
        )

        logs_layout.addWidget(
            self.status,
            1
        )

        operation_area_layout.addWidget(
            logs_card,
            7
        )

        main_layout.addWidget(
            operation_area,
            1
        )

        # ======================================================
        # SQL STATISTICS
        # ======================================================

        statistics_card = QFrame()

        statistics_card.setObjectName(
            "SqlStatisticsCard"
        )

        statistics_card.setStyleSheet(
            """
            QFrame#SqlStatisticsCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        statistics_layout = QVBoxLayout(
            statistics_card
        )

        statistics_layout.setContentsMargins(
            16,
            14,
            16,
            16
        )

        statistics_layout.setSpacing(
            8
        )

        statistics_title = QLabel(
            "SQL Statistics"
        )

        statistics_title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:11pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        statistics_layout.addWidget(
            statistics_title
        )

        statistics_accent = QLabel()

        statistics_accent.setFixedHeight(
            3
        )

        statistics_accent.setStyleSheet(
            """
            QLabel {
                background:#FF9800;
                border:none;
            }
            """
        )

        statistics_layout.addWidget(
            statistics_accent
        )

        statistics_row = QHBoxLayout()

        statistics_row.setSpacing(
            18
        )

        self.operation_db_value = (
            self._create_stat_value(
                "-"
            )
        )

        self.affected_rows_value = (
            self._create_stat_value(
                "-"
            )
        )

        self.operation_result_value = (
            self._create_stat_value(
                "Ready"
            )
        )

        self.operation_time_value = (
            self._create_stat_value(
                "--"
            )
        )

        statistics_row.addWidget(
            self._create_stat(
                "Database",
                self.operation_db_value
            )
        )

        statistics_row.addWidget(
            self._create_stat(
                "Affected Rows",
                self.affected_rows_value
            )
        )

        statistics_row.addWidget(
            self._create_stat(
                "Result",
                self.operation_result_value
            )
        )

        statistics_row.addWidget(
            self._create_stat(
                "Status",
                self.operation_time_value
            )
        )

        statistics_layout.addLayout(
            statistics_row
        )

        main_layout.addWidget(
            statistics_card
        )

        # ======================================================
        # INITIAL DATABASE
        # ======================================================

        active_database = (
            database_context.active()
        )

        if active_database:

            self.on_database_changed(
                active_database
            )

    # ==========================================================
    # ACTION BUTTON
    # ==========================================================

    def create_action_button(
        self,
        text,
        icon_path,
        accent,
    ):

        button = QPushButton()

        button.setObjectName(
            "SqlActionButton"
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setMinimumHeight(
            32
        )

        layout = QHBoxLayout(
            button
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            6
        )

        icon = SvgIcon(
            icon_path,
            size=17
        )

        label = QLabel(
            text
        )

        label.setStyleSheet(
            f"""
            QLabel {{
                background:transparent;
                border:none;
                color:{accent};
                font-size:9pt;
                font-weight:600;
            }}
            """
        )

        layout.addWidget(
            icon
        )

        layout.addWidget(
            label
        )

        layout.addStretch()

        button.setStyleSheet(
            """
            QPushButton#SqlActionButton {
                background:transparent;
                border:none;
                outline:none;
                padding:0;
                margin:0;
            }

            QPushButton#SqlActionButton:hover {
                background:transparent;
                border:none;
                outline:none;
            }

            QPushButton#SqlActionButton:pressed {
                background:transparent;
                border:none;
                outline:none;
            }

            QPushButton#SqlActionButton:focus {
                background:transparent;
                border:none;
                outline:none;
            }

            QPushButton#SqlActionButton:disabled {
                background:transparent;
                border:none;
                outline:none;
            }
            """
        )

        return button

    # ==========================================================
    # STAT
    # ==========================================================

    def _create_stat_value(
        self,
        text
    ):

        label = QLabel(
            text
        )

        label.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:9pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        return label

    def _create_stat(
        self,
        title,
        value
    ):

        widget = QWidget()

        layout = QVBoxLayout(
            widget
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            2
        )

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:8pt;
                background:transparent;
                border:none;
            }
            """
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value
        )

        return widget

    # ==========================================================
    # DATABASE
    # ==========================================================

    def on_database_changed(
        self,
        database,
    ):

        if not database:

            self.database_name_value.setText(
                "Not selected"
            )

            self.database_server_value.setText(
                "-"
            )

            self.database_state_value.setText(
                "Not Connected"
            )

            self.operation_db_value.setText(
                "-"
            )

            return

        name = database.get(
            "name",
            "Unknown"
        )

        server = database.get(
            "server",
            "Unknown"
        )

        self.database_name_value.setText(
            name
        )

        self.database_server_value.setText(
            server
        )

        self.database_state_value.setText(
            "Connected"
        )

        self.database_state_value.setStyleSheet(
            """
            QLabel {
                color:#53C653;
                font-size:9pt;
                font-weight:700;
                background:transparent;
                border:none;
            }
            """
        )

        self.operation_db_value.setText(
            name
        )

        self.append_status(
            ""
        )

        self.append_status(
            f"Database selected: {name}"
        )

        self.append_status(
            f"Server: {server}"
        )

    # ==========================================================
    # HELPERS
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

            affected_rows = result.get(
                "affected_rows",
                -1,
            )

            if affected_rows >= 0:

                self.append_status(
                    f"Affected Rows: "
                    f"{affected_rows}"
                )

                self.affected_rows_value.setText(
                    str(
                        affected_rows
                    )
                )

            self.operation_state_value.setText(
                "Completed"
            )

            self.operation_result_value.setText(
                "Success"
            )

            self.database_state_value.setText(
                "Connected"
            )

            self.operation_task.setText(
                f"{result['step']} completed successfully."
            )

        else:

            self.append_status(
                f"✗ {result['step']} failed."
            )

            self.append_status(
                result["message"]
            )

            self.operation_state_value.setText(
                "Failed"
            )

            self.operation_result_value.setText(
                "Failed"
            )

            self.database_state_value.setText(
                "Operation failed"
            )

            self.operation_task.setText(
                f"{result['step']} failed."
            )

    # ==========================================================
    # OPERATIONS
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

            self.append_status(
                ""
            )

            self.append_status(
                "Δεν έχει επιλεγεί βάση δεδομένων."
            )

            self.append_status(
                "Παρακαλώ επίλεξε βάση από το Dashboard."
            )

            return

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

        self.operation_value.setText(
            title
        )

        self.operation_db_value.setText(
            database.get(
                "name",
                "Unknown"
            )
        )

        self.operation_state_value.setText(
            "Running"
        )

        self.operation_task.setText(
            f"Running {title}..."
        )

        self.operation_result_value.setText(
            "Running"
        )

        self.affected_rows_value.setText(
            "-"
        )

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
    # STARTED
    # ==========================================================

    def on_started(
        self
    ):

        pass

    # ==========================================================
    # FINISHED
    # ==========================================================

    def on_finished(
        self,
        result,
    ):

        self.show_result(
            result
        )

    # ==========================================================
    # ERROR
    # ==========================================================

    def on_error(
        self,
        message,
    ):

        self.append_status(
            f"✗ Error: {message}"
        )

        self.operation_state_value.setText(
            "Failed"
        )

        self.operation_result_value.setText(
            "Failed"
        )

        self.operation_task.setText(
            "SQL operation failed."
        )

    # ==========================================================
    # THREAD FINISHED
    # ==========================================================

    def on_thread_finished(
        self
    ):

        self.append_status(
            ""
        )

        self.append_status(
            "Ready."
        )

        if (
            self.operation_state_value.text()
            not in {
                "Completed",
                "Failed",
            }
        ):

            self.operation_state_value.setText(
                "Ready"
            )

        self.set_buttons_enabled(
            True
        )

        self.current_operation = None
        self.controller = None
        self.thread = None

    # ==========================================================
    # DELETE MYDATA RESPONSE
    # ==========================================================

    def delete_mydata_response(
        self
    ):

        self.start_operation(
            "delete",
            "Delete MyDATA Response",
        )

    # ==========================================================
    # REBUILD DATABASE
    # ==========================================================

    def rebuild_database(
        self
    ):

        self.start_operation(
            "rebuild",
            "Rebuild Database",
        )

    # ==========================================================
    # SHRINK DATABASE
    # ==========================================================

    def shrink_database(
        self
    ):

        self.start_operation(
            "shrink",
            "Shrink Database",
        )