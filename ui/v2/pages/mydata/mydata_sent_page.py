from PySide6.QtCore import Qt, QDate, QObject, QThread, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QAbstractItemView,
    QApplication,
    QProgressBar,
    QPlainTextEdit,
)

from core.mydata.mydata_service import MyDataService
from core.mydata.mydata_pdf import MyDataPDF
from core.database.database_context import database_context


class MyDataSendWorker(QObject):

    progress = Signal(
        int,
        int,
        object,
        dict,
    )

    finished = Signal(
        list
    )

    failed = Signal(
        str
    )

    def __init__(
        self,
        service,
        invoices,
    ):

        super().__init__()

        self.service = service
        self.invoices = list(
            invoices
        )

    def run(
        self,
    ):

        results = []

        total = len(
            self.invoices
        )

        try:

            for index, invoice in enumerate(
                self.invoices,
                start=1,
            ):

                self.progress.emit(
                    index - 1,
                    total,
                    invoice,
                    {
                        "success": False,
                        "status_code": None,
                        "message": "",
                        "started": True,
                    },
                )

                try:

                    result = self.service.send_invoice(
                        invoice.invoice_id
                    )

                    invoice.send_status = (
                        result.get(
                            "status_code"
                        )
                    )

                    invoice.send_message = (
                        result.get(
                            "message",
                            ""
                        )
                        or ""
                    )

                    invoice.sent = bool(
                        result.get(
                            "success",
                            False,
                        )
                    )

                except Exception as exc:

                    invoice.sent = False
                    invoice.send_status = None
                    invoice.send_message = str(
                        exc
                    )

                    result = {
                        "success": False,
                        "status_code": None,
                        "message": str(
                            exc
                        ),
                    }

                item = {
                    "invoice": invoice,
                    "result": result,
                }

                results.append(
                    item
                )

                self.progress.emit(
                    index,
                    total,
                    invoice,
                    result,
                )

            self.finished.emit(
                results
            )

        except Exception as exc:

            self.failed.emit(
                str(
                    exc
                )
            )


class MyDataSentPage(QWidget):

    def __init__(
        self,
    ):

        super().__init__()

        self.service = MyDataService()

        self.invoices = []

        self._send_thread = None
        self._send_worker = None

        self.setup_ui()

        self._clear_failure_details()

        database_context.database_changed.connect(
            self.update_connection_status
        )

        self.update_connection_status(
            database_context.active()
        )

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(
        self,
    ):

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            20,
            18,
            20,
            22,
        )

        root.setSpacing(
            14
        )

        # ======================================================
        # HEADER
        # ======================================================

        header = QHBoxLayout()

        title_block = QVBoxLayout()

        title_block.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        title_block.setSpacing(
            2
        )

        title = QLabel(
            "myDATA Manager"
        )

        title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:24pt;
                font-weight:700;
                border:none;
            }
            """
        )

        subtitle = QLabel(
            "Check, validate and send documents to myDATA"
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:10pt;
                border:none;
            }
            """
        )

        title_block.addWidget(
            title
        )

        title_block.addWidget(
            subtitle
        )

        header.addLayout(
            title_block
        )

        header.addStretch()

        self.connection_status = QLabel(
            "Not Connected"
        )

        self.connection_status.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        header.addWidget(
            self.connection_status
        )

        root.addLayout(
            header
        )

        # ======================================================
        # SEARCH CARD
        # ======================================================

        search_card = QWidget()

        search_card.setObjectName(
            "SearchCard"
        )

        search_card.setStyleSheet(
            """
            QWidget#SearchCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        search_layout = QVBoxLayout(
            search_card
        )

        search_layout.setContentsMargins(
            14,
            12,
            14,
            14,
        )

        search_layout.setSpacing(
            10
        )

        search_title = QLabel(
            "Search Documents"
        )

        search_title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:10pt;
                font-weight:700;
            }
            """
        )

        search_layout.addWidget(
            search_title
        )

        search_accent = QLabel()

        search_accent.setFixedHeight(
            3
        )

        search_accent.setStyleSheet(
            """
            QLabel {
                background:#29A8FF;
                border:none;
            }
            """
        )

        search_layout.addWidget(
            search_accent
        )

        # ======================================================
        # DATE FILTERS
        # ======================================================

        controls = QHBoxLayout()

        controls.setContentsMargins(
            0,
            0,
            0,
            0
        )

        controls.setSpacing(
            8
        )

        from_label = QLabel(
            "From"
        )

        from_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                font-weight:600;
            }
            """
        )

        self.from_date = QDateEdit()

        self.from_date.setCalendarPopup(
            True
        )

        self.from_date.setDate(
            QDate.currentDate().addMonths(
                -1
            )
        )

        self.from_date.setDisplayFormat(
            "dd/MM/yyyy"
        )

        to_label = QLabel(
            "To"
        )

        to_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                font-weight:600;
            }
            """
        )

        self.to_date = QDateEdit()

        self.to_date.setCalendarPopup(
            True
        )

        self.to_date.setDate(
            QDate.currentDate()
        )

        self.to_date.setDisplayFormat(
            "dd/MM/yyyy"
        )

        date_style = """
            QDateEdit {
                background:#202226;
                color:#F4F5F7;
                border:1px solid #3A3D43;
                padding:6px 9px;
                min-height:32px;
            }

            QDateEdit:focus {
                border:1px solid #29A8FF;
            }
        """

        self.from_date.setStyleSheet(
            date_style
        )

        self.to_date.setStyleSheet(
            date_style
        )

        self.search_button = QPushButton(
            "▶  Search"
        )

        self.search_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.search_button.setMinimumHeight(
            36
        )

        self.search_button.setMinimumWidth(
            100
        )

        self.search_button.setStyleSheet(
            """
            QPushButton {
                background:transparent;
                color:#E53935;
                border:none;
                padding:0 8px;
                font-size:10pt;
                font-weight:700;
            }

            QPushButton:hover {
                color:#FF4B4B;
            }

            QPushButton:pressed {
                color:#C62828;
            }

            QPushButton:disabled {
                color:#666A71;
            }
            """
        )

        self.search_button.clicked.connect(
            self.search
        )

        controls.addWidget(
            from_label
        )

        controls.addWidget(
            self.from_date
        )

        controls.addWidget(
            to_label
        )

        controls.addWidget(
            self.to_date
        )

        controls.addWidget(
            self.search_button
        )

        controls.addStretch()

        search_layout.addLayout(
            controls
        )

        root.addWidget(
            search_card
        )

        # ======================================================
        # ACTION BAR
        # ======================================================

        actions = QHBoxLayout()

        actions.setContentsMargins(
            2,
            0,
            2,
            0
        )

        actions.setSpacing(
            18
        )

        self.select_all_button = self._action_button(
            "□  Select All",
            "#E6E8EC",
            115
        )

        self.send_selected_button = self._action_button(
            "▶  Send Selected",
            "#E53935",
            135
        )

        self.send_all_button = self._action_button(
            "▶  Send All",
            "#E6E8EC",
            105
        )

        self.delete_button = self._action_button(
            "■  Delete M.A.R.K.",
            "#FF9800",
            135
        )

        self.pdf_button = self._action_button(
            "▣  Export PDF",
            "#E6E8EC",
            115
        )

        self.select_all_button.clicked.connect(
            self.select_all
        )

        self.send_selected_button.clicked.connect(
            self.send_selected
        )

        self.send_all_button.clicked.connect(
            self.send_all
        )

        self.delete_button.clicked.connect(
            self.delete_mydata
        )

        self.pdf_button.clicked.connect(
            self.print_pdf
        )

        actions.addWidget(
            self.select_all_button
        )

        actions.addWidget(
            self.send_selected_button
        )

        actions.addWidget(
            self.send_all_button
        )

        actions.addWidget(
            self.delete_button
        )

        actions.addWidget(
            self.pdf_button
        )

        actions.addStretch()

        root.addLayout(
            actions
        )

        # ======================================================
        # SEND PROGRESS
        # ======================================================

        self.send_progress_card = QWidget()

        self.send_progress_card.setObjectName(
            "SendProgressCard"
        )

        self.send_progress_card.setStyleSheet(
            """
            QWidget#SendProgressCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        progress_layout = QVBoxLayout(
            self.send_progress_card
        )

        progress_layout.setContentsMargins(
            12,
            8,
            12,
            8
        )

        progress_layout.setSpacing(
            5
        )

        progress_header = QHBoxLayout()

        self.send_progress_title = QLabel(
            "Ready."
        )

        self.send_progress_title.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#F4F5F7;
                font-size:9pt;
                font-weight:700;
            }
            """
        )

        self.send_progress_count = QLabel(
            "0 / 0"
        )

        self.send_progress_count.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#9FA4AE;
                font-size:8.5pt;
                font-weight:600;
            }
            """
        )

        progress_header.addWidget(
            self.send_progress_title
        )

        progress_header.addStretch()

        progress_header.addWidget(
            self.send_progress_count
        )

        progress_layout.addLayout(
            progress_header
        )

        self.send_progress_bar = QProgressBar()

        self.send_progress_bar.setRange(
            0,
            100
        )

        self.send_progress_bar.setValue(
            0
        )

        self.send_progress_bar.setTextVisible(
            False
        )

        self.send_progress_bar.setFixedHeight(
            7
        )

        self.send_progress_bar.setStyleSheet(
            """
            QProgressBar {
                background:#202226;
                border:none;
                border-radius:3px;
            }

            QProgressBar::chunk {
                background:#29A8FF;
                border-radius:3px;
            }
            """
        )

        progress_layout.addWidget(
            self.send_progress_bar
        )

        self.send_progress_detail = QLabel(
            ""
        )

        self.send_progress_detail.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#9FA4AE;
                font-size:8pt;
            }
            """
        )

        progress_layout.addWidget(
            self.send_progress_detail
        )

        self.send_progress_card.hide()

        root.addWidget(
            self.send_progress_card
        )

        # ======================================================
        # FAILURE DETAILS
        # ======================================================

        self.failure_card = QWidget()

        self.failure_card.setObjectName(
            "FailureCard"
        )

        self.failure_card.setStyleSheet(
            """
            QWidget#FailureCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        failure_layout = QVBoxLayout(
            self.failure_card
        )

        failure_layout.setContentsMargins(
            12,
            8,
            12,
            8
        )

        failure_layout.setSpacing(
            5
        )

        failure_header = QHBoxLayout()

        failure_title = QLabel(
            "Failed Documents"
        )

        failure_title.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#F4F5F7;
                font-size:9pt;
                font-weight:700;
            }
            """
        )

        self.failure_count_label = QLabel(
            "0 failed"
        )

        self.failure_count_label.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#FF5252;
                font-size:8.5pt;
                font-weight:700;
            }
            """
        )

        failure_header.addWidget(
            failure_title
        )

        failure_header.addStretch()

        failure_header.addWidget(
            self.failure_count_label
        )

        failure_layout.addLayout(
            failure_header
        )

        failure_accent = QLabel()

        failure_accent.setFixedHeight(
            3
        )

        failure_accent.setStyleSheet(
            """
            QLabel {
                background:#E53935;
                border:none;
            }
            """
        )

        failure_layout.addWidget(
            failure_accent
        )

        self.failure_details = QPlainTextEdit()

        self.failure_details.setReadOnly(
            True
        )

        self.failure_details.setMinimumHeight(
            90
        )

        self.failure_details.setMaximumHeight(
            170
        )

        self.failure_details.setStyleSheet(
            """
            QPlainTextEdit {
                background:#202226;
                border:1px solid #35383F;
                color:#F4F5F7;
                padding:8px;
                font-size:8.5pt;
            }

            QScrollBar:vertical {
                background:#202226;
                width:10px;
            }

            QScrollBar::handle:vertical {
                background:#494D55;
                min-height:30px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height:0px;
                border:none;
            }
            """
        )

        failure_layout.addWidget(
            self.failure_details
        )

        self.failure_card.hide()

        root.addWidget(
            self.failure_card
        )

        # ======================================================
        # DOCUMENTS CARD
        # ======================================================

        documents_card = QWidget()

        documents_card.setObjectName(
            "DocumentsCard"
        )

        documents_card.setStyleSheet(
            """
            QWidget#DocumentsCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        documents_layout = QVBoxLayout(
            documents_card
        )

        documents_layout.setContentsMargins(
            14,
            12,
            14,
            14
        )

        documents_layout.setSpacing(
            8
        )

        documents_header = QHBoxLayout()

        documents_title = QLabel(
            "Documents"
        )

        documents_title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:10pt;
                font-weight:700;
            }
            """
        )

        self.count_label = QLabel(
            "0 documents"
        )

        self.count_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
            }
            """
        )

        documents_header.addWidget(
            documents_title
        )

        documents_header.addStretch()

        documents_header.addWidget(
            self.count_label
        )

        documents_layout.addLayout(
            documents_header
        )

        table_accent = QLabel()

        table_accent.setFixedHeight(
            3
        )

        table_accent.setStyleSheet(
            """
            QLabel {
                background:#29A8FF;
                border:none;
            }
            """
        )

        documents_layout.addWidget(
            table_accent
        )

        # ======================================================
        # TABLE
        # ======================================================

        self.table = QTableWidget()

        self.table.setColumnCount(
            8
        )

        self.table.setHorizontalHeaderLabels(
            [
                "",
                "Type",
                "Document",
                "Date",
                "A/A",
                "VAT No.",
                "ID",
                "Status",
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.table.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )

        self.table.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )

        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.table.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        self.table.setMouseTracking(
            True
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setShowGrid(
            False
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setStyleSheet(
            """
            QTableWidget {
                background:#202226;
                alternate-background-color:#24272C;
                color:#E6E8EC;
                border:1px solid #35383F;
                selection-background-color:#30343B;
                selection-color:#FFFFFF;
            }

            QHeaderView::section {
                background:#1D1F23;
                color:#9FA4AE;
                border:none;
                border-bottom:1px solid #3A3D43;
                padding:9px 8px;
                font-size:8pt;
                font-weight:700;
            }

            QTableWidget::item {
                border-bottom:1px solid #303238;
                padding:7px 8px;
            }

            QTableWidget::item:selected {
                background:#30343B;
                color:#FFFFFF;
            }

            QScrollBar:vertical {
                background:#202226;
                width:10px;
                margin:0;
            }

            QScrollBar::handle:vertical {
                background:#494D55;
                min-height:35px;
            }

            QScrollBar::handle:vertical:hover {
                background:#5A5F68;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height:0px;
                background:none;
                border:none;
            }

            QScrollBar:horizontal {
                background:#202226;
                height:10px;
                margin:0;
            }

            QScrollBar::handle:horizontal {
                background:#494D55;
                min-width:35px;
            }

            QScrollBar::handle:horizontal:hover {
                background:#5A5F68;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width:0px;
                background:none;
                border:none;
            }
            """
        )

        header_view = (
            self.table.horizontalHeader()
        )

        header_view.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header_view.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header_view.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.Stretch
        )

        header_view.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header_view.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header_view.setSectionResizeMode(
            5,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header_view.setSectionResizeMode(
            6,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header_view.setSectionResizeMode(
            7,
            QHeaderView.ResizeMode.ResizeToContents
        )

        documents_layout.addWidget(
            self.table,
            1
        )

        root.addWidget(
            documents_card,
            1
        )

        # ======================================================
        # STATUS
        # ======================================================

        self.status_label = QLabel(
            "Ready."
        )

        self.status_label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                background:#202226;
                border:1px solid #34373D;
                padding:7px 10px;
                font-size:8.5pt;
            }
            """
        )

        root.addWidget(
            self.status_label
        )

    # ==========================================================
    # ACTION BUTTON
    # ==========================================================

    def _action_button(
        self,
        text,
        color,
        width,
    ):

        button = QPushButton(
            text
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setMinimumHeight(
            38
        )

        button.setMinimumWidth(
            width
        )

        button.setStyleSheet(
            f"""
            QPushButton {{
                background:transparent;
                color:{color};
                border:none;
                padding:0;
                margin:0;
                font-size:10pt;
                font-weight:600;
                text-align:left;
            }}

            QPushButton:hover {{
                background:transparent;
                color:#FFFFFF;
            }}

            QPushButton:pressed {{
                background:transparent;
            }}

            QPushButton:disabled {{
                background:transparent;
                color:#666A71;
            }}
            """
        )

        return button

    # ==========================================================
    # CONNECTION STATUS
    # ==========================================================

    def update_connection_status(
        self,
        database,
    ):

        if database:

            self.connection_status.setText(
                "Connected"
            )

            self.connection_status.setStyleSheet(
                """
                QLabel {
                    color:#53C653;
                    font-size:9pt;
                    font-weight:700;
                    background:transparent;
                    border:none;
                    padding:0;
                }
                """
            )

        else:

            self.connection_status.setText(
                "Not Connected"
            )

            self.connection_status.setStyleSheet(
                """
                QLabel {
                    color:#FF9800;
                    font-size:9pt;
                    font-weight:700;
                    background:transparent;
                    border:none;
                    padding:0;
                }
                """
            )

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(
        self,
    ):

        start = self.from_date.date().toString(
            "yyyyMMdd"
        )

        end = self.to_date.date().toString(
            "yyyyMMdd"
        )

        if start > end:

            QMessageBox.warning(
                self,
                "myDATA Manager",
                "The From date cannot be later than the To date.",
            )

            return

        if not self.service.database_selected():

            QMessageBox.warning(
                self,
                "myDATA Manager",
                "No database has been selected.",
            )

            return

        self.status_label.setText(
            "Searching documents..."
        )

        QApplication.processEvents()

        try:

            self.invoices = (
                self.service.search(
                    start,
                    end,
                )
            )

            self.populate_table()

            self.status_label.setText(
                "Search completed."
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Search Error",
                str(
                    exc
                ),
            )

            self.status_label.setText(
                "Search failed."
            )

    # ==========================================================
    # TABLE
    # ==========================================================

    def populate_table(
        self,
    ):

        self.table.setRowCount(
            0
        )

        for row_index, invoice in enumerate(
            self.invoices
        ):

            self.table.insertRow(
                row_index
            )

            checkbox = QTableWidgetItem()

            checkbox.setFlags(
                checkbox.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )

            checkbox.setCheckState(
                Qt.CheckState.Unchecked
            )

            self.table.setItem(
                row_index,
                0,
                checkbox,
            )

            values = [
                invoice.invoice_type,
                invoice.document_name,
                invoice.issue_date,
                invoice.aa,
                invoice.cust_afm,
                str(invoice.invoice_id),
            ]

            for column, value in enumerate(
                values,
                start=1,
            ):

                self.table.setItem(
                    row_index,
                    column,
                    QTableWidgetItem(
                        str(
                            value
                        )
                    )
                )

            status_item = QTableWidgetItem(
                "SENT"
                if invoice.sent
                else "PENDING"
            )

            status_item.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            if invoice.sent:

                status_item.setForeground(
                    Qt.GlobalColor.green
                )

            else:

                status_item.setForeground(
                    Qt.GlobalColor.yellow
                )

            self.table.setItem(
                row_index,
                7,
                status_item,
            )

        self.table.clearSelection()

        self.count_label.setText(
            f"{len(self.invoices)} documents"
        )

        self.table.setCurrentCell(
            -1,
            -1
        )

        self.table.setFocus()

    # ==========================================================
    # SELECT ALL
    # ==========================================================

    def select_all(
        self,
    ):

        if not self.invoices:

            return

        all_checked = True

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0
            )

            if (
                item
                and item.checkState()
                != Qt.CheckState.Checked
            ):

                all_checked = False
                break

        target_state = (
            Qt.CheckState.Unchecked
            if all_checked
            else Qt.CheckState.Checked
        )

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0
            )

            if item:

                item.setCheckState(
                    target_state
                )

        self.select_all_button.setText(
            "□  Clear Selection"
            if target_state
            == Qt.CheckState.Checked
            else "□  Select All"
        )

    # ==========================================================
    # SELECTED
    # ==========================================================

    def get_selected_invoices(
        self,
    ):

        selected = []

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0
            )

            if (
                item
                and item.checkState()
                == Qt.CheckState.Checked
            ):

                if row < len(
                    self.invoices
                ):

                    selected.append(
                        self.invoices[
                            row
                        ]
                    )

        return selected

    # ==========================================================
    # SEND SELECTED
    # ==========================================================

    def send_selected(
        self,
    ):

        invoices = (
            self.get_selected_invoices()
        )

        if not invoices:

            QMessageBox.information(
                self,
                "myDATA Manager",
                "No documents have been selected.",
            )

            return

        self.send_invoices(
            invoices
        )

    # ==========================================================
    # SEND ALL
    # ==========================================================

    def send_all(
        self,
    ):

        if not self.invoices:

            QMessageBox.information(
                self,
                "myDATA Manager",
                "There are no documents to send.",
            )

            return

        answer = QMessageBox.question(
            self,
            "Send All",
            (
                f"Send all {len(self.invoices)} "
                "documents?"
            ),
        )

        if (
            answer
            != QMessageBox.StandardButton.Yes
        ):

            return

        self.send_invoices(
            self.invoices
        )

    # ==========================================================
    # SEND
    # ==========================================================

    def send_invoices(
        self,
        invoices,
    ):

        if (
            self._send_thread
            and self._send_thread.isRunning()
        ):

            return

        invoices = list(
            invoices
        )

        if not invoices:

            return

        total = len(
            invoices
        )

        self._clear_failure_details()

        self.send_progress_card.show()

        self.send_progress_bar.setValue(
            0
        )

        self.send_progress_count.setText(
            f"0 / {total}"
        )

        self.send_progress_title.setText(
            "Sending documents..."
        )

        self.send_progress_detail.setText(
            ""
        )

        self.status_label.setText(
            f"Sending 0 / {total}..."
        )

        self.send_selected_button.setEnabled(
            False
        )

        self.send_all_button.setEnabled(
            False
        )

        self.search_button.setEnabled(
            False
        )

        QApplication.setOverrideCursor(
            Qt.CursorShape.WaitCursor
        )

        self._send_thread = QThread(
            self
        )

        self._send_worker = MyDataSendWorker(
            self.service,
            invoices,
        )

        self._send_worker.moveToThread(
            self._send_thread
        )

        self._send_thread.started.connect(
            self._send_worker.run
        )

        self._send_worker.progress.connect(
            self._on_send_progress
        )

        self._send_worker.finished.connect(
            self._on_send_finished
        )

        self._send_worker.failed.connect(
            self._on_send_worker_error
        )

        self._send_worker.finished.connect(
            self._send_thread.quit
        )

        self._send_worker.failed.connect(
            self._send_thread.quit
        )

        self._send_thread.finished.connect(
            self._on_send_thread_finished
        )

        self._send_thread.start()

    def _find_invoice_row(
        self,
        invoice,
    ):

        for row, current in enumerate(
            self.invoices
        ):

            if (
                current.invoice_id
                == invoice.invoice_id
            ):

                return row

        return -1

    def _on_send_progress(
        self,
        index,
        total,
        invoice,
        result,
    ):

        percentage = (
            int(
                (
                    index
                    / total
                )
                * 100
            )
            if total
            else 0
        )

        self.send_progress_bar.setValue(
            percentage
        )

        self.send_progress_count.setText(
            f"{index} / {total}"
        )

        aa = (
            invoice.aa
            or "-"
        )

        document_name = (
            invoice.document_name
            or "Document"
        )

        self.send_progress_title.setText(
            "Sending document..."
            if index < total
            else "Sending completed."
        )

        self.send_progress_detail.setText(
            (
                f"{document_name} | "
                f"A/A: {aa}"
            )
        )

        self.status_label.setText(
            (
                f"Sending {index} / {total}..."
                if index < total
                else
                f"Processed {total} / {total}..."
            )
        )

        if index > 0:

            row = self._find_invoice_row(
                invoice
            )

            if row >= 0:

                status_item = (
                    self.table.item(
                        row,
                        7
                    )
                )

                if status_item:

                    if result.get(
                        "success",
                        False,
                    ):

                        status_item.setText(
                            "SENT"
                        )

                        status_item.setForeground(
                            Qt.GlobalColor.green
                        )

                        status_item.setToolTip(
                            "Document sent successfully."
                        )

                    else:

                        message = (
                            result.get(
                                "message",
                                "",
                            )
                            or invoice.send_message
                            or "Unknown error."
                        )

                        status_code = (
                            result.get(
                                "status_code"
                            )
                        )

                        status_item.setText(
                            "FAILED"
                        )

                        status_item.setForeground(
                            Qt.GlobalColor.red
                        )

                        status_item.setToolTip(
                            (
                                f"HTTP {status_code}\n"
                                f"{message}"
                                if status_code
                                else message
                            )
                        )

        QApplication.processEvents()

    def _on_send_finished(
        self,
        results,
    ):

        success_count = sum(
            1
            for item in results
            if item["result"].get(
                "success",
                False,
            )
        )

        failed_items = [
            item
            for item in results
            if not item["result"].get(
                "success",
                False,
            )
        ]

        failed_count = len(
            failed_items
        )

        self.send_progress_bar.setValue(
            100
        )

        self.send_progress_count.setText(
            (
                f"{len(results)} / "
                f"{len(results)}"
            )
        )

        self.send_progress_title.setText(
            "Sending completed."
        )

        self.send_progress_detail.setText(
            (
                f"Successful: {success_count} | "
                f"Failed: {failed_count}"
            )
        )

        self.status_label.setText(
            (
                f"Completed: "
                f"{success_count} successful, "
                f"{failed_count} failed."
            )
        )

        self.update_table_after_send()

        self.send_selected_button.setEnabled(
            True
        )

        self.send_all_button.setEnabled(
            True
        )

        self.search_button.setEnabled(
            True
        )

        QApplication.restoreOverrideCursor()

        if failed_count:

            failure_lines = []

            for item in failed_items:

                invoice = item["invoice"]
                result = item["result"]

                aa = (
                    invoice.aa
                    or "-"
                )

                document_name = (
                    invoice.document_name
                    or "Document"
                )

                status_code = (
                    result.get(
                        "status_code"
                    )
                    or "-"
                )

                message = (
                    result.get(
                        "message"
                    )
                    or invoice.send_message
                    or "Unknown error."
                )

                failure_lines.append(
                    (
                        f"A/A {aa} - {document_name}\n"
                        f"HTTP: {status_code}\n"
                        f"{message}"
                    )
                )

            details = (
                "\n\n".join(
                    failure_lines
                )
            )

            self._show_failure_details(
                failed_items
            )

            QMessageBox.warning(
                self,
                "myDATA Manager",
                (
                    "Sending completed.\n\n"
                    f"Successful: {success_count}\n"
                    f"Failed: {failed_count}\n\n"
                    "Failure details:\n"
                    f"{details}"
                ),
            )

        else:

            self._clear_failure_details()

            QMessageBox.information(
                self,
                "myDATA Manager",
                (
                    "All documents were sent "
                    f"successfully: {success_count}."
                ),
            )

    def _show_failure_details(
        self,
        failed_items,
    ):

        lines = []

        for item in failed_items:

            invoice = item["invoice"]
            result = item["result"]

            aa = (
                invoice.aa
                or "-"
            )

            document_name = (
                invoice.document_name
                or "Document"
            )

            status_code = (
                result.get(
                    "status_code"
                )
                or "-"
            )

            message = (
                result.get(
                    "message"
                )
                or invoice.send_message
                or "Unknown error."
            )

            lines.append(
                (
                    f"A/A: {aa}\n"
                    f"Document: {document_name}\n"
                    f"HTTP: {status_code}\n"
                    f"Error: {message}"
                )
            )

        self.failure_details.setPlainText(
            "\n\n".join(
                lines
            )
        )

        self.failure_count_label.setText(
            f"{len(failed_items)} failed"
        )

        self.failure_card.show()

    def _clear_failure_details(
        self,
    ):

        if not hasattr(
            self,
            "failure_card",
        ):

            return

        self.failure_details.clear()

        self.failure_count_label.setText(
            "0 failed"
        )

        self.failure_card.hide()

    def _on_send_worker_error(
        self,
        message,
    ):

        QApplication.restoreOverrideCursor()

        self.send_progress_title.setText(
            "Sending failed."
        )

        self.send_progress_detail.setText(
            str(
                message
            )
        )

        self.status_label.setText(
            "Sending failed."
        )

        self.send_selected_button.setEnabled(
            True
        )

        self.send_all_button.setEnabled(
            True
        )

        self.search_button.setEnabled(
            True
        )

        QMessageBox.critical(
            self,
            "Send Error",
            str(
                message
            ),
        )

    def _on_send_thread_finished(
        self,
    ):

        thread = self._send_thread
        worker = self._send_worker

        self._send_thread = None
        self._send_worker = None

        if worker:

            worker.deleteLater()

        if thread:

            thread.deleteLater()

    # ==========================================================
    # UPDATE TABLE
    # ==========================================================

    def update_table_after_send(
        self,
    ):

        for row, invoice in enumerate(
            self.invoices
        ):

            checkbox = self.table.item(
                row,
                0
            )

            if (
                checkbox
                and invoice.sent
            ):

                checkbox.setCheckState(
                    Qt.CheckState.Unchecked
                )

            status_item = self.table.item(
                row,
                7
            )

            if not status_item:

                continue

            if invoice.sent:

                status_item.setText(
                    "SENT"
                )

                status_item.setForeground(
                    Qt.GlobalColor.green
                )

                status_item.setToolTip(
                    "Document sent successfully."
                )

            else:

                status_item.setText(
                    "FAILED"
                )

                status_item.setForeground(
                    Qt.GlobalColor.red
                )

                status_item.setToolTip(
                    invoice.send_message
                    or "Unknown sending error."
                )

        self.select_all_button.setText(
            "□  Select All"
        )

    # ==========================================================
    # DELETE M.A.R.K.
    # ==========================================================

    def delete_mydata(
        self,
    ):

        QMessageBox.information(
            self,
            "Delete M.A.R.K.",
            (
                "The M.A.R.K. delete operation "
                "will be handled by the existing service."
            ),
        )

    # ==========================================================
    # PDF
    # ==========================================================

    def print_pdf(
        self,
    ):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.information(
                self,
                "Export PDF",
                "Select a document first.",
            )

            return

        if row >= len(
            self.invoices
        ):

            return

        invoice = self.invoices[
            row
        ]

        if not invoice.sent:

            QMessageBox.warning(
                self,
                "Export PDF",
                (
                    "The document must be sent "
                    "successfully before exporting PDF."
                ),
            )

            return

        try:

            success = MyDataPDF.save_invoice(
                invoice,
                self,
            )

            if success:

                self.status_label.setText(
                    "PDF exported successfully."
                )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "PDF Error",
                str(
                    exc
                )
            )