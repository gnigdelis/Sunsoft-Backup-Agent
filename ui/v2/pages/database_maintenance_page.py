from PySide6.QtCore import (
    QDate,
    QThread,
    Qt,
 )

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
    QDateEdit,
    QProgressBar,
    QSizePolicy,
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
        self.current_operation_parameters = {}

        self.operation_progress = 0

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

        self.sales_trans_move_button = (
            self.create_action_button(
                "▶  Move Sales To Hist",
                Icons.HISTORY,
                "#53C653",
            )
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

        self.extra_lock_button = (
            self.create_action_button(
                "Extra Lock",
                Icons.CLOCK,
                "#AB47BC",
            )
        )

        actions_layout.addWidget(
            self.sales_trans_move_button
        )

        actions_layout.addWidget(
            self.delete_button
        )

        actions_layout.addWidget(
            self.rebuild_button
        )

        actions_layout.addWidget(
            self.shrink_button
        )

        actions_layout.addWidget(
            self.extra_lock_button
        )

        actions_layout.addStretch()

        main_layout.addLayout(
            actions_layout
        )

        self.sales_trans_move_button.clicked.connect(
            self.move_sales_to_hist
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

        # ======================================================
        # SALES TRANS MOVE
        # ======================================================

        sales_move_panel = QFrame()

        sales_move_panel.setObjectName(
            "SalesMovePanel"
        )

        sales_move_panel.setStyleSheet(
            """
            QFrame#SalesMovePanel {
                background:#25262B;
                border:1px solid #393C43;
            }

            QLabel {
                background:transparent;
                border:none;
            }

            QDateEdit {
                background:#1E1F23;
                color:#F4F5F7;
                border:1px solid #44474F;
                padding:5px 8px;
                min-height:28px;
            }
            """
        )

        sales_move_layout = QVBoxLayout(
            sales_move_panel
        )

        sales_move_layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        sales_move_layout.setSpacing(
            8
        )

        sales_title = QLabel(
            "Move Sales To Hist"
        )

        sales_title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:11pt;
                font-weight:700;
            }
            """
        )

        sales_move_layout.addWidget(
            sales_title
        )

        sales_dates = QHBoxLayout()

        from_label = QLabel(
            "From"
        )

        from_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
            }
            """
        )

        self.sales_from_date = QDateEdit()

        self.sales_from_date.setCalendarPopup(
            True
        )

        self.sales_from_date.setDate(
            QDate.currentDate()
        )

        to_label = QLabel(
            "To"
        )

        to_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
            }
            """
        )

        self.sales_to_date = QDateEdit()

        self.sales_to_date.setCalendarPopup(
            True
        )

        self.sales_to_date.setDate(
            QDate.currentDate()
        )

        self.sales_move_go_button = QPushButton(
            "GO"
        )

        self.sales_move_go_button.setObjectName(
            "SalesMoveGoButton"
        )

        self.sales_move_go_button.setFixedHeight(
            30
        )

        self.sales_move_go_button.setMinimumWidth(
            70
        )

        self.sales_move_go_button.setStyleSheet(
            """
            QPushButton#SalesMoveGoButton {
                background:#19391E;
                color:#70E34A;
                border:1px solid #53C653;
                font-weight:700;
                padding:4px 14px;
            }

            QPushButton#SalesMoveGoButton:hover {
                background:#214A27;
                border:1px solid #70E34A;
            }

            QPushButton#SalesMoveGoButton:disabled {
                background:#181818;
                color:#555A63;
                border:1px solid #292C31;
            }
            """
        )

        sales_dates.addWidget(
            from_label
        )

        sales_dates.addWidget(
            self.sales_from_date
        )

        sales_dates.addSpacing(
            10
        )

        sales_dates.addWidget(
            to_label
        )

        sales_dates.addWidget(
            self.sales_to_date
        )

        sales_dates.addSpacing(
            10
        )

        sales_dates.addWidget(
            self.sales_move_go_button
        )

        sales_dates.addStretch()

        sales_move_layout.addLayout(
            sales_dates
        )

        main_layout.addWidget(
            sales_move_panel
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
            16,
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

        # ======================================================
        # CURRENT OPERATION
        # ======================================================

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

        # ======================================================
        # DATABASE
        # ======================================================

        operation_db_row = QHBoxLayout()

        db_label = QLabel(
            "Database"
        )

        db_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                background:transparent;
                border:none;
            }
            """
        )

        self.operation_db_value = QLabel(
            "-"
        )

        self.operation_db_value.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.operation_db_value.setStyleSheet(
            """
            QLabel {
                color:#D9DCE2;
                font-size:9pt;
                background:transparent;
                border:none;
            }
            """
        )

        operation_db_row.addWidget(
            db_label
        )

        operation_db_row.addStretch()

        operation_db_row.addWidget(
            self.operation_db_value
        )

        operation_layout.addLayout(
            operation_db_row
        )

        # ======================================================
        # STATE
        # ======================================================

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

        # ======================================================
        # TASK
        # ======================================================

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

        # ======================================================
        # PROGRESS
        # ======================================================

        progress_row = QHBoxLayout()

        progress_label = QLabel(
            "Progress"
        )

        progress_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                background:transparent;
                border:none;
            }
            """
        )

        self.operation_progress_bar = QProgressBar()

        self.operation_progress_bar.setObjectName(
            "OperationProgressBar"
        )

        self.operation_progress_bar.setRange(
            0,
            100,
        )

        self.operation_progress_bar.setValue(
            0
        )

        self.operation_progress_bar.setTextVisible(
            True
        )

        self.operation_progress_bar.setFormat(
            "%p%"
        )

        self.operation_progress_bar.setFixedHeight(
            14
        )

        self.operation_progress_bar.setStyleSheet(
            """
            QProgressBar#OperationProgressBar {
                background:#202226;
                color:#D9DCE2;
                border:1px solid #393C43;
                text-align:center;
                font-size:8pt;
                font-weight:700;
            }

            QProgressBar#OperationProgressBar::chunk {
                background:#29A8FF;
            }
            """
        )

        progress_row.addWidget(
            progress_label
        )

        progress_row.addWidget(
            self.operation_progress_bar,
            1,
        )

        operation_layout.addLayout(
            progress_row
        )

        # ======================================================
        # STOP
        # ======================================================

        stop_row = QHBoxLayout()

        stop_row.addStretch()

        self.stop_button = QPushButton(
            "■   STOP"
        )

        self.stop_button.setObjectName(
            "SqlStopButton"
        )

        self.stop_button.setFixedHeight(
            32
        )

        self.stop_button.setMinimumWidth(
            100
        )

        self.stop_button.setEnabled(
            False
        )

        self.stop_button.setStyleSheet(
            """
            QPushButton#SqlStopButton {
                background:#3A1717;
                color:#FF6B6B;
                border:1px solid #E53935;
                font-weight:700;
                padding:4px 16px;
            }

            QPushButton#SqlStopButton:hover {
                background:#4A1D1D;
                border:1px solid #FF5A5A;
            }

            QPushButton#SqlStopButton:pressed {
                background:#2A1010;
            }

            QPushButton#SqlStopButton:disabled {
                background:#202125;
                color:#555A63;
                border:1px solid #333438;
            }
            """
        )

        stop_row.addWidget(
            self.stop_button
        )

        operation_layout.addLayout(
            stop_row
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
            0,
        )

        operation_area_layout.setSpacing(
            14
        )

        # ======================================================
        # LIVE LOG
        # ======================================================

        live_log_card = QFrame()

        live_log_card.setObjectName(
            "LiveLogCard"
        )

        live_log_card.setStyleSheet(
            """
            QFrame#LiveLogCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        live_log_layout = QVBoxLayout(
            live_log_card
        )

        live_log_layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        live_log_layout.setSpacing(
            8
        )

        live_log_title = QLabel(
            "Live Logs"
        )

        live_log_title.setStyleSheet(
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

        live_log_layout.addWidget(
            live_log_title
        )

        self.status = QTextEdit()

        self.status.setReadOnly(
            True
        )

        self.status.setMinimumHeight(
            180
        )

        self.status.setStyleSheet(
            """
            QTextEdit {
                background:#18191D;
                color:#D9DCE2;
                border:1px solid #393C43;
                padding:8px;
                font-size:9pt;
            }
            """
        )

        live_log_layout.addWidget(
            self.status
        )

        operation_area_layout.addWidget(
            live_log_card,
            2,
        )

        # ======================================================
        # STATISTICS
        # ======================================================

        statistics_card = QFrame()

        statistics_card.setObjectName(
            "StatisticsCard"
        )

        statistics_card.setStyleSheet(
            """
            QFrame#StatisticsCard {
                background:#25262B;
                border:1px solid #393C43;
            }

            QLabel {
                background:transparent;
                border:none;
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
            14,
        )

        statistics_layout.setSpacing(
            12
        )

        statistics_title = QLabel(
            "Statistics"
        )

        statistics_title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:10pt;
                font-weight:700;
            }
            """
        )

        statistics_layout.addWidget(
            statistics_title
        )

        self.affected_rows_value = QLabel(
            "-"
        )

        self.affected_rows_value.setStyleSheet(
            """
            QLabel {
                color:#D9DCE2;
                font-size:16pt;
                font-weight:700;
            }
            """
        )

        statistics_layout.addWidget(
            QLabel(
                "Affected Rows"
            )
        )

        statistics_layout.addWidget(
            self.affected_rows_value
        )

        statistics_layout.addStretch()

        operation_area_layout.addWidget(
            statistics_card,
            1,
        )

        main_layout.addWidget(
            operation_area,
            1,
        )

        # ======================================================
        # SIGNALS
        # ======================================================

        self.stop_button.clicked.connect(
            self.stop_operation
        )

        self.sales_move_go_button.clicked.connect(
            self.move_sales_to_hist
        )

    # ==========================================================
    # ACTION BUTTON
    # ==========================================================

    def create_action_button(
        self,
        text,
        icon,
        accent,
    ):

        button = QPushButton()

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setMinimumHeight(
            42
        )

        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        button_layout = QHBoxLayout(
            button
        )

        button_layout.setContentsMargins(
            4,
            2,
            4,
            2
        )

        button_layout.setSpacing(
            8
        )

        icon_widget = SvgIcon(
            icon,
            20
        )

        button_layout.addWidget(
            icon_widget
        )

        text_label = QLabel(
            text
        )

        text_label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        text_label.setStyleSheet(
            f"""
            QLabel {{
                color: {accent};
                background: transparent;
                border: none;
                font-size: 10pt;
                font-weight: 700;
            }}
            """
        )

        button_layout.addWidget(
            text_label
        )

        button_layout.addStretch()

        button.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                padding: 0px;
                text-align: left;
            }}

            QPushButton:hover {{
                background: transparent;
                border: none;
            }}

            QPushButton:pressed {{
                background: transparent;
                border: none;
            }}

            QPushButton:disabled {{
                background: transparent;
                border: none;
            }}
            """
        )

        return button

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
    # EXTRA LOCK
    # ==========================================================

    def open_extra_lock(
        self,
    ):

        if not database_context.is_selected():

            self.append_status(
                ""
            )

            self.append_status(
                "Ξ”ΞµΞ½ Ξ­Ο‡ΞµΞΉ ΞµΟ€ΞΉΞ»ΞµΞ³ΞµΞ― Ξ²Ξ¬ΟƒΞ· Ξ΄ΞµΞ΄ΞΏΞΌΞ­Ξ½Ο‰Ξ½."
            )

            self.append_status(
                "Ξ Ξ±ΟΞ±ΞΊΞ±Ξ»Ο ΞµΟ€Ξ―Ξ»ΞµΞΎΞµ Ξ²Ξ¬ΟƒΞ· Ξ±Ο€Ο Ο„ΞΏ Dashboard."
            )

            return

        if not hasattr(
            self,
            "extra_lock_page",
        ):

            return

        if self.extra_lock_page.isVisible():

            self.extra_lock_page.hide()

            self.extra_lock_button.setText(
                "Extra Lock"
            )

            return

        self.extra_lock_page.load_values()

        self.extra_lock_page.show()

        self.extra_lock_button.setText(
            "Close Extra Lock"
        )

    # ==========================================================
    # STOP
    # ==========================================================

    def stop_operation(
        self,
    ):

        if self.controller is None:

            return

        if self.current_operation is None:

            return

        self.stop_button.setEnabled(
            False
        )

        self.operation_state_value.setText(
            "Stopping..."
        )

        self.operation_task.setText(
            "Cancelling SQL operation..."
        )

        self.append_status(
            ""
        )

        self.append_status(
            "■  Stop requested by user."
        )

        self.controller.stop()

    # ==========================================================
    # BUTTON STATE
    # ==========================================================

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

        self.extra_lock_button.setEnabled(
            enabled
        )

        self.sales_trans_move_button.setEnabled(
            enabled
        )

        self.sales_move_go_button.setEnabled(
            enabled
        )

    # ==========================================================
    # OPERATION START
    # ==========================================================

    def start_operation(
        self,
        operation,
        title,
        parameters=None,
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
                "Ξ”ΞµΞ½ Ξ­Ο‡ΞµΞΉ ΞµΟ€ΞΉΞ»ΞµΞ³ΞµΞ― Ξ²Ξ¬ΟƒΞ· Ξ΄ΞµΞ΄ΞΏΞΌΞ­Ξ½Ο‰Ξ½."
            )

            self.append_status(
                "Ξ Ξ±ΟΞ±ΞΊΞ±Ξ»Ο ΞµΟ€Ξ―Ξ»ΞµΞΎΞµ Ξ²Ξ¬ΟƒΞ· Ξ±Ο€Ο Ο„ΞΏ Dashboard."
            )

            return

        self.set_buttons_enabled(
            False
        )

        self.stop_button.setEnabled(
            True
        )

        self.current_operation = (
            operation
        )

        self.current_operation_parameters = (
            parameters or {}
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
                "Unknown",
            )
        )

        self.operation_state_value.setText(
            "Running"
        )

        self.operation_task.setText(
            f"Running {title}..."
        )

        self.operation_progress = 0

        self.operation_progress_bar.setRange(
            0,
            100,
        )

        self.operation_progress_bar.setValue(
            0
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

        self.controller.progress.connect(
            self.on_progress
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
        self,
    ):

        pass

    # ==========================================================
    # PROGRESS
    # ==========================================================

    def on_progress(
        self,
        percent,
        message,
    ):

        percent = max(
            0,
            min(
                int(percent),
                100,
            ),
        )

        self.operation_progress = (
            percent
        )

        self.operation_progress_bar.setValue(
            percent
        )

        if message:

            self.operation_task.setText(
                str(message)
            )

            lines = (
                self.status
                .toPlainText()
                .splitlines()
            )

            if not lines or lines[-1] != str(
                message
            ):

                self.append_status(
                    str(message)
                )

    # ==========================================================
    # FINISHED
    # ==========================================================

    def on_finished(
        self,
        result,
    ):

        if result["success"]:

            self.operation_state_value.setText(
                "Completed"
            )

            self.operation_task.setText(
                f"{result['step']} completed successfully."
            )

            self.operation_progress_bar.setValue(
                100
            )

            self.append_status(
                ""
            )

            self.append_status(
                f"β“ {result['step']} "
                f"completed successfully."
            )

        else:

            message = str(
                result.get(
                    "message",
                    "",
                )
            )

            if "cancelled" in message.lower():

                self.operation_state_value.setText(
                    "Cancelled"
                )

                self.operation_task.setText(
                    "SQL operation cancelled."
                )

                self.append_status(
                    ""
                )

                self.append_status(
                    "■  Operation cancelled."
                )

            else:

                self.operation_state_value.setText(
                    "Failed"
                )

                self.operation_task.setText(
                    f"{result['step']} failed."
                )

                self.append_status(
                    ""
                )

                self.append_status(
                    f"β— {result['step']} failed."
                )

                if message:

                    self.append_status(
                        message
                    )

        affected_rows = result.get(
            "affected_rows",
            0,
        )

        if affected_rows is None:

            affected_rows = 0

        self.affected_rows_value.setText(
            str(
                affected_rows
            )
        )

    # ==========================================================
    # ERROR
    # ==========================================================

    def on_error(
        self,
        message,
    ):

        self.operation_state_value.setText(
            "Failed"
        )

        self.operation_task.setText(
            "SQL operation failed."
        )

        self.append_status(
            ""
        )

        self.append_status(
            f"β— Error: {message}"
        )

    # ==========================================================
    # THREAD FINISHED
    # ==========================================================

    def on_thread_finished(
        self,
    ):

        self.append_status(
            ""
        )

        self.append_status(
            "Ready."
        )

        self.set_buttons_enabled(
            True
        )

        self.stop_button.setEnabled(
            False
        )

        self.current_operation = None

        self.controller = None

        self.thread = None

    # ==========================================================
    # DELETE MYDATA
    # ==========================================================

    def delete_mydata_response(
        self,
    ):

        self.start_operation(
            "delete",
            "Delete MyDATA Response",
        )

    # ==========================================================
    # REBUILD
    # ==========================================================

    def rebuild_database(
        self,
    ):

        self.start_operation(
            "rebuild",
            "Rebuild Database",
        )

    # ==========================================================
    # SHRINK
    # ==========================================================

    def shrink_database(
        self,
    ):

        self.start_operation(
            "shrink",
            "Shrink Database",
        )

    # ==========================================================
    # SALES TRANS MOVE
    # ==========================================================

    def move_sales_to_hist(
        self,
    ):

        self.append_status(
            ""
        )

        self.append_status(
            "Move Sales To Hist"
        )

        # The existing SalesTrans Move implementation
        # should remain connected here.
        #
        # Date values are available through:
        #
        # self.sales_from_date.date()
        # self.sales_to_date.date()

    # ==========================================================
    # STATUS
    # ==========================================================

    def append_status(
        self,
        message,
    ):

        self.status.append(
            str(message)
        )




