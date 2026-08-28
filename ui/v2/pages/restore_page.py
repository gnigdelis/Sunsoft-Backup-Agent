from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QThread,
)

from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ui.v2.styles.theme import Theme

from core.services.restore_service import restore_service
from core.controllers.restore_controller import RestoreController


class RestorePage(QWidget):

    def __init__(self):

        super().__init__()

        self.thread = None
        self.controller = None
        self.backup_file = None

        self.setup_ui()

    # ==========================================================
    # CARD
    # ==========================================================

    def make_card(
        self,
        title,
    ):

        card = QFrame()

        card.setStyleSheet(
            f"""
            QFrame {{
                background:{Theme.Colors.SURFACE};
                border:1px solid {Theme.Colors.BORDER};
                border-radius:8px;
            }}

            QFrame QLabel {{
                background:transparent;
                border:none;
            }}
            """
        )

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            16,
            14,
            16,
            16,
        )

        layout.setSpacing(
            10
        )

        label = QLabel(
            title
        )

        label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:11pt;
                font-weight:700;
                background:transparent;
                border:none;
            }}
            """
        )

        layout.addWidget(
            label
        )

        accent = QLabel()

        accent.setFixedHeight(
            3
        )

        accent.setStyleSheet(
            """
            QLabel {
                background:#E53935;
                border:none;
            }
            """
        )

        layout.addWidget(
            accent
        )

        return card, layout

    # ==========================================================
    # ACTION BUTTON
    # ==========================================================

    def make_action_button(
        self,
        text,
        accent="#E53935",
    ):

        button = QPushButton(
            text
        )

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setMinimumHeight(
            34
        )

        button.setStyleSheet(
            f"""
            QPushButton {{
                background:transparent;
                border:none;
                color:{accent};
                font-size:9pt;
                font-weight:700;
                padding:4px 8px;
            }}

            QPushButton:hover {{
                color:{accent};
            }}

            QPushButton:disabled {{
                color:#666A72;
            }}
            """
        )

        return button

    # ==========================================================
    # INFO ROW
    # ==========================================================

    def make_info_row(
        self,
        caption,
        value="-",
    ):

        row = QHBoxLayout()

        row.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        left = QLabel(
            caption
        )

        left.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
                background:transparent;
                border:none;
            }}
            """
        )

        right = QLabel(
            value
        )

        right.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        right.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:9pt;
                font-weight:600;
                background:transparent;
                border:none;
            }}
            """
        )

        row.addWidget(
            left
        )

        row.addStretch()

        row.addWidget(
            right
        )

        return row, right

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(
        self,
    ):

        self.setObjectName(
            "RestorePage"
        )

        self.setStyleSheet(
            """
            QWidget#RestorePage {
                background:transparent;
                border:none;
            }

            QWidget#RestorePage QLabel {
                background:transparent;
                border:none;
            }

            QCheckBox {
                color:#F4F5F7;
                background:#202226;
                border:none;
                padding:4px 6px;
                font-size:9pt;
            }

            QCheckBox::indicator {
                width:13px;
                height:13px;
            }

            QTextEdit {
                background:#17181B;
                color:#D9DCE2;
                border:1px solid #393C43;
                font-size:9pt;
            }
            """
        )

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
            16
        )

        # ======================================================
        # HEADER
        # ======================================================

        header = QHBoxLayout()

        header.setContentsMargins(
            0,
            0,
            0,
            4,
        )

        title_block = QVBoxLayout()

        title_block.setSpacing(
            2
        )

        title = QLabel(
            "Restore"
        )

        title.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                background:transparent;
                border:none;
                font-size:24pt;
                font-weight:700;
                padding:0;
            }}
            """
        )

        subtitle = QLabel(
            "Restore and recover your system from a backup"
        )

        subtitle.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                background:transparent;
                border:none;
                font-size:10pt;
                padding:0;
            }}
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

        self.status = QLabel(
            "Ready"
        )

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.status.setMinimumWidth(
            120
        )

        self.status.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#53C653;
                font-size:10pt;
                font-weight:700;
                padding:0 4px;
            }
            """
        )

        header.addWidget(
            self.status
        )

        root.addLayout(
            header
        )

        # ======================================================
        # RESTORE ACTIONS
        # ======================================================

        actions_header = QLabel(
            "Restore Actions"
        )

        actions_header.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:9pt;
                font-weight:700;
                background:transparent;
                border:none;
            }}
            """
        )

        root.addWidget(
            actions_header
        )

        actions = QHBoxLayout()

        actions.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        actions.setSpacing(
            18
        )

        self.browse_button = self.make_action_button(
            "▣  Browse Backup",
            "#F4F5F7",
        )

        self.browse_button.clicked.connect(
            self.select_backup
        )

        self.restore_button = self.make_action_button(
            "▶  Restore",
            "#E53935",
        )

        self.restore_button.setEnabled(
            False
        )

        self.restore_button.clicked.connect(
            self.start_restore
        )

        self.stop_button = self.make_action_button(
            "■  Stop",
            "#E53935",
        )

        self.stop_button.setEnabled(
            False
        )

        self.stop_button.clicked.connect(
            self.stop_restore
        )

        actions.addWidget(
            self.browse_button
        )

        actions.addWidget(
            self.restore_button
        )

        actions.addWidget(
            self.stop_button
        )

        actions.addStretch()

        root.addLayout(
            actions
        )

        # ======================================================
        # BACKUP INFORMATION
        # ======================================================

        backup_card, backup_layout = self.make_card(
            "Backup Information"
        )

        self.backup_name_value = QLabel(
            "-"
        )

        self.backup_size_value = QLabel(
            "-"
        )

        self.database_count_value = QLabel(
            "-"
        )

        self.registry_count_value = QLabel(
            "-"
        )

        self.printers_value = QLabel(
            "-"
        )

        for caption, value in [
            ("Backup", self.backup_name_value),
            ("Size", self.backup_size_value),
            ("Databases", self.database_count_value),
            ("Registry", self.registry_count_value),
            ("Printers", self.printers_value),
        ]:

            row = QHBoxLayout()

            left = QLabel(
                caption
            )

            left.setStyleSheet(
                f"""
                QLabel {{
                    color:{Theme.Colors.TEXT_SECONDARY};
                    font-size:9pt;
                }}
                """
            )

            value.setStyleSheet(
                f"""
                QLabel {{
                    color:{Theme.Colors.TEXT};
                    font-size:9pt;
                    font-weight:600;
                }}
                """
            )

            row.addWidget(
                left
            )

            row.addStretch()

            row.addWidget(
                value
            )

            backup_layout.addLayout(
                row
            )

        self.backup_path_value = QLabel(
            "No backup selected."
        )

        self.backup_path_value.setWordWrap(
            True
        )

        self.backup_path_value.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:8pt;
                padding-top:4px;
            }}
            """
        )

        backup_layout.addWidget(
            self.backup_path_value
        )

        root.addWidget(
            backup_card
        )

        # ======================================================
        # RESTORE CONTENTS
        # ======================================================

        contents_card, contents_layout = self.make_card(
            "Restore Contents"
        )

        checks = QHBoxLayout()

        checks.setSpacing(
            8
        )

        self.database_check = QCheckBox(
            "Database"
        )

        self.files_check = QCheckBox(
            "Application / Configuration Files"
        )

        self.registry_check = QCheckBox(
            "Registry Settings"
        )

        self.printers_check = QCheckBox(
            "Printers"
        )

        self.database_check.setChecked(
            True
        )

        self.files_check.setChecked(
            True
        )

        self.registry_check.setChecked(
            True
        )

        self.printers_check.setChecked(
            True
        )

        checks.addWidget(
            self.database_check
        )

        checks.addWidget(
            self.files_check
        )

        checks.addWidget(
            self.registry_check
        )

        checks.addWidget(
            self.printers_check
        )

        checks.addStretch()

        contents_layout.addLayout(
            checks
        )

        root.addWidget(
            contents_card
        )

        # ======================================================
        # PROGRESS
        # ======================================================

        progress_card, progress_layout = self.make_card(
            "Restore Progress"
        )

        progress_header = QHBoxLayout()

        progress_label = QLabel(
            "Progress"
        )

        progress_label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        self.progress_percent = QLabel(
            "0%"
        )

        self.progress_percent.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        self.progress_percent.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:9pt;
                font-weight:700;
            }
            """
        )

        progress_header.addWidget(
            progress_label
        )

        progress_header.addStretch()

        progress_header.addWidget(
            self.progress_percent
        )

        progress_layout.addLayout(
            progress_header
        )

        self.progress_bar = QProgressBar()

        self.progress_bar.setRange(
            0,
            100,
        )

        self.progress_bar.setValue(
            0
        )

        self.progress_bar.setTextVisible(
            False
        )

        self.progress_bar.setFixedHeight(
            12
        )

        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                background:#393C43;
                border:none;
            }

            QProgressBar::chunk {
                background:#29A8FF;
            }
            """
        )

        progress_layout.addWidget(
            self.progress_bar
        )

        self.current_task = QLabel(
            "Waiting..."
        )

        self.current_task.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:9pt;
                font-weight:600;
                padding-top:3px;
            }}
            """
        )

        progress_layout.addWidget(
            self.current_task
        )

        root.addWidget(
            progress_card
        )

        # ======================================================
        # LOWER AREA
        # ======================================================

        middle = QHBoxLayout()

        middle.setContentsMargins(
            0,
            4,
            0,
            4,
        )

        middle.setSpacing(
            18
        )

        # ------------------------------------------------------
        # OPERATION STATUS
        # ------------------------------------------------------

        operation_card, operation_layout = self.make_card(
            "Restore Status"
        )

        self.operation_value = QLabel(
            "Ready"
        )

        self.operation_value.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:10pt;
                font-weight:700;
            }}
            """
        )

        operation_layout.addWidget(
            self.operation_value
        )

        self.selection_value = QLabel(
            "No backup selected."
        )

        self.selection_value.setWordWrap(
            True
        )

        self.selection_value.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
            """
        )

        operation_layout.addWidget(
            self.selection_value
        )

        operation_layout.addStretch()

        middle.addWidget(
            operation_card,
            1,
        )

        # ------------------------------------------------------
        # LIVE LOGS
        # ------------------------------------------------------

        logs_card, logs_layout = self.make_card(
            "Live Logs"
        )

        self.log = QTextEdit()

        self.log.setReadOnly(
            True
        )

        self.log.setMinimumHeight(
            120
        )

        logs_layout.addWidget(
            self.log
        )

        middle.addWidget(
            logs_card,
            2,
        )

        root.addLayout(
            middle,
            1,
        )

        # ======================================================
        # STATISTICS
        # ======================================================

        statistics_card, statistics_layout = self.make_card(
            "Restore Statistics"
        )

        statistics_row = QHBoxLayout()

        self.database_stat = self.make_stat(
            "Databases"
        )

        self.files_stat = self.make_stat(
            "Files"
        )

        self.registry_stat = self.make_stat(
            "Registry"
        )

        self.printers_stat = self.make_stat(
            "Printers"
        )

        for widget in [
            self.database_stat[0],
            self.files_stat[0],
            self.registry_stat[0],
            self.printers_stat[0],
        ]:

            statistics_row.addWidget(
                widget
            )

        statistics_layout.addLayout(
            statistics_row
        )

        root.addWidget(
            statistics_card
        )

    # ==========================================================
    # STATISTIC
    # ==========================================================

    def make_stat(
        self,
        title,
    ):

        container = QWidget()

        layout = QVBoxLayout(
            container
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        label = QLabel(
            title
        )

        label.setStyleSheet(
            f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:8pt;
            }}
            """
        )

        value = QLabel(
            "-"
        )

        value.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:10pt;
                font-weight:700;
            }
            """
        )

        layout.addWidget(
            label
        )

        layout.addWidget(
            value
        )

        return container, value

    # ==========================================================
    # SELECT BACKUP
    # ==========================================================

    def select_backup(
        self,
    ):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Backup",
            "",
            "Sunsoft Backup (*.zip);;All Files (*)",
        )

        if not file_path:
            return

        try:

            info = restore_service.inspect(
                file_path
            )

            self.backup_file = file_path

            self.backup_path_value.setText(
                file_path
            )

            self.selection_value.setText(
                Path(file_path).name
            )

            self.backup_name_value.setText(
                info["backup_name"]
            )

            size_mb = (
                info["backup_size"]
                / 1024
                / 1024
            )

            self.backup_size_value.setText(
                f"{size_mb:.2f} MB"
            )

            self.database_count_value.setText(
                str(len(info["sql"]))
            )

            self.registry_count_value.setText(
                str(len(info["registry"]))
            )

            self.printers_value.setText(
                "Yes"
                if info["printers"]
                else "No"
            )

            self.status.setText(
                "Ready"
            )

            self.operation_value.setText(
                "Backup verified"
            )

            self.current_task.setText(
                "Backup ready for restore."
            )

            self.restore_button.setEnabled(
                True
            )

            self.append_log(
                "Backup selected and verified."
            )

        except Exception as ex:

            self.backup_file = None

            self.restore_button.setEnabled(
                False
            )

            self.status.setText(
                "Error"
            )

            QMessageBox.critical(
                self,
                "Backup Error",
                str(ex),
            )

    # ==========================================================
    # START RESTORE
    # ==========================================================

    def start_restore(
        self,
    ):

        if not self.backup_file:
            return

        if not any(
            [
                self.database_check.isChecked(),
                self.files_check.isChecked(),
                self.registry_check.isChecked(),
                self.printers_check.isChecked(),
            ]
        ):

            QMessageBox.warning(
                self,
                "Restore",
                "Select at least one restore option.",
            )

            return

        answer = QMessageBox.warning(
            self,
            "Confirm Restore",
            (
                "The selected backup contents will be restored.\n\n"
                "Existing files, registry settings and databases "
                "may be replaced.\n\n"
                "Do you want to continue?"
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.set_running(
            True
        )

        self.progress_bar.setValue(
            0
        )

        self.progress_percent.setText(
            "0%"
        )

        self.current_task.setText(
            "Starting restore..."
        )

        self.operation_value.setText(
            "Restore running"
        )

        self.status.setText(
            "Running"
        )

        self.log.clear()

        self.append_log(
            "Starting restore..."
        )

        self.thread = QThread(
            self
        )

        self.controller = RestoreController(
            restore_service,
            self.thread,
            self.backup_file,
            self.database_check.isChecked(),
            self.files_check.isChecked(),
            self.registry_check.isChecked(),
            self.printers_check.isChecked(),
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

        self.status.setText(
            "Running"
        )

        self.operation_value.setText(
            "Restore running"
        )

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

        self.progress_bar.setValue(
            percent
        )

        self.progress_percent.setText(
            f"{percent}%"
        )

        if message:

            message = str(
                message
            )

            self.current_task.setText(
                message
            )

            self.append_log(
                message
            )

    # ==========================================================
    # FINISHED
    # ==========================================================

    def on_finished(
        self,
        result,
    ):

        self.progress_bar.setValue(
            100
        )

        self.progress_percent.setText(
            "100%"
        )

        self.current_task.setText(
            "Restore completed successfully."
        )

        self.operation_value.setText(
            "Completed"
        )

        self.status.setText(
            "Ready"
        )

        self.append_log(
            "Restore completed successfully."
        )

        self.set_running(
            False
        )

        if isinstance(
            result,
            dict,
        ):

            self.database_stat[1].setText(
                str(
                    result.get(
                        "database",
                        0,
                    )
                )
            )

            self.files_stat[1].setText(
                str(
                    result.get(
                        "files",
                        0,
                    )
                )
            )

            self.registry_stat[1].setText(
                str(
                    result.get(
                        "registry",
                        0,
                    )
                )
            )

            self.printers_stat[1].setText(
                "Restored"
                if result.get(
                    "printers",
                    False,
                )
                else "Not restored"
            )

        QMessageBox.information(
            self,
            "Restore",
            "Restore completed successfully.",
        )

    # ==========================================================
    # ERROR
    # ==========================================================

    def on_error(
        self,
        message,
    ):

        self.current_task.setText(
            "Restore failed."
        )

        self.operation_value.setText(
            "Failed"
        )

        self.status.setText(
            "Error"
        )

        self.append_log(
            f"ERROR: {message}"
        )

        self.set_running(
            False
        )

        QMessageBox.critical(
            self,
            "Restore Error",
            str(message),
        )

    # ==========================================================
    # STOP
    # ==========================================================

    def stop_restore(
        self,
    ):

        if not self.controller:
            return

        self.append_log(
            "Cancellation requested..."
        )

        self.current_task.setText(
            "Stopping..."
        )

        self.operation_value.setText(
            "Stopping"
        )

        self.controller.stop()

        self.stop_button.setEnabled(
            False
        )

    # ==========================================================
    # RUNNING STATE
    # ==========================================================

    def set_running(
        self,
        running,
    ):

        self.browse_button.setEnabled(
            not running
        )

        self.restore_button.setEnabled(
            not running
            and bool(
                self.backup_file
            )
        )

        self.stop_button.setEnabled(
            running
        )

        self.database_check.setEnabled(
            not running
        )

        self.files_check.setEnabled(
            not running
        )

        self.registry_check.setEnabled(
            not running
        )

        self.printers_check.setEnabled(
            not running
        )

    # ==========================================================
    # LOG
    # ==========================================================

    def append_log(
        self,
        message,
    ):

        self.log.append(
            str(message)
        )

    # ==========================================================
    # THREAD FINISHED
    # ==========================================================

    def on_thread_finished(
        self,
    ):

        self.thread = None
        self.controller = None
