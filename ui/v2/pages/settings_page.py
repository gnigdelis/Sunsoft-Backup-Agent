from pathlib import Path

from PySide6.QtCore import Qt, QTime
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QFrame,
    QComboBox,
    QTimeEdit,
    QCheckBox,
)

from core.destination_manager import DestinationManager
from core.scheduler.backup_scheduler import BackupScheduler
from core.providers.pcloud_provider import PCloudProvider



class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.destination_manager = DestinationManager()
        self.scheduler = BackupScheduler(self)

        self._build_ui()
        self._load_settings()
        self._load_schedule()

        self.scheduler.schedule_changed.connect(
            self._update_schedule_status
        )

        self.scheduler.backup_triggered.connect(
            self._scheduled_backup_started
        )

    # ==========================================================
    # UI
    # ==========================================================

    def _build_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 22)
        layout.setSpacing(14)

        header = QVBoxLayout()
        header.setSpacing(2)

        title = QLabel("Settings")
        title.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:24pt;
                font-weight:700;
                background:transparent;
                border:none;
                padding:0;
            }
            """
        )

        subtitle = QLabel(
            "Configure backup destination and automatic backup schedule"
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:10pt;
                background:transparent;
                border:none;
                padding:0;
            }
            """
        )

        header.addWidget(title)
        header.addWidget(subtitle)

        layout.addLayout(header)

        cards_row = QHBoxLayout()
        cards_row.setContentsMargins(0, 0, 0, 0)
        cards_row.setSpacing(16)

        destination_card = self._create_card(
            "Backup Destination",
            "#00ACC1",
        )

        schedule_card = self._create_card(
            "Scheduled Backup",
            "#FF9800",
        )

        cards_row.addWidget(destination_card, 1)
        cards_row.addWidget(schedule_card, 1)

        layout.addLayout(cards_row)
        layout.addStretch()

        self._build_destination_card(
            destination_card.layout()
        )

        self._build_schedule_card(
            schedule_card.layout()
        )

    # ==========================================================
    # DESTINATION CARD
    # ==========================================================

    def _build_destination_card(self, card_layout):

        description = QLabel(
            "Select where backup files will be stored."
        )

        self._muted_label(description)
        card_layout.addWidget(description)

        destination_row = QHBoxLayout()
        destination_row.setContentsMargins(0, 2, 0, 0)
        destination_row.setSpacing(10)

        self.destination_input = QLineEdit()
        self.destination_input.setReadOnly(True)
        self.destination_input.setMinimumHeight(38)

        self.destination_input.setStyleSheet(
            """
            QLineEdit {
                background:#202226;
                color:#F4F5F7;
                border:1px solid #3A3D43;
                padding:0 10px;
                font-size:9pt;
                selection-background-color:#30343B;
            }

            QLineEdit:focus {
                border:1px solid #29A8FF;
            }
            """
        )

        destination_row.addWidget(
            self.destination_input,
            1,
        )

        self.browse_button = self._flat_button(
            "Browse...",
            "#F4F5F7",
        )

        self.browse_button.clicked.connect(
            self._browse_destination
        )

        destination_row.addWidget(
            self.browse_button
        )

        card_layout.addLayout(destination_row)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 2, 0, 0)
        actions.setSpacing(18)

        self.save_button = self._flat_button(
            "Save",
            "#E53935",
        )

        self.test_button = self._flat_button(
            "Test Destination",
            "#29A8FF",
        )

        self.reset_button = self._flat_button(
            "Reset to Default",
            "#FF9800",
        )

        self.save_button.clicked.connect(
            self._save_destination
        )

        self.test_button.clicked.connect(
            lambda: self._test_destination(
                show_message=True
            )
        )

        self.reset_button.clicked.connect(
            self._reset_destination
        )

        actions.addWidget(self.save_button)
        actions.addWidget(self.test_button)
        actions.addWidget(self.reset_button)
        actions.addStretch()

        card_layout.addLayout(actions)

        self.status_label = QLabel(
            "Status: Unknown"
        )

        self._status_label_style(
            self.status_label,
            "#9FA4AE",
        )

        card_layout.addWidget(
            self.status_label
        )

        self.storage_label = QLabel("")
        self._muted_label(
            self.storage_label
        )

        card_layout.addWidget(
            self.storage_label
        )

        card_layout.addStretch()

    # ==========================================================
    # SCHEDULE CARD
    # ==========================================================

    def _build_schedule_card(self, card_layout):

        description = QLabel(
            "Automatically run backups according to the configured schedule."
        )

        self._muted_label(description)
        card_layout.addWidget(description)

        enable_row = QHBoxLayout()
        enable_row.setContentsMargins(
            0,
            6,
            0,
            0,
        )

        enable_label = QLabel(
            "Automatic Backup"
        )

        self._field_label(
            enable_label
        )

        self.schedule_enabled = QCheckBox()

        self.schedule_enabled.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.schedule_enabled.setToolTip(
            "Enable or disable automatic backups"
        )

        self.schedule_enabled.setStyleSheet(
            """
            QCheckBox {
                background:transparent;
                border:none;
            }

            QCheckBox::indicator {
                width:40px;
                height:22px;
                border-radius:11px;
            }

            QCheckBox::indicator:unchecked {
                background:#33363C;
                border:1px solid #555A63;
            }

            QCheckBox::indicator:checked {
                background:#53C653;
                border:1px solid #53C653;
            }
            """
        )

        enable_row.addWidget(
            enable_label
        )

        enable_row.addStretch()

        enable_row.addWidget(
            self.schedule_enabled
        )

        card_layout.addLayout(
            enable_row
        )

        fields = QGridLayout()
        fields.setContentsMargins(
            0,
            6,
            0,
            0,
        )

        fields.setHorizontalSpacing(18)
        fields.setVerticalSpacing(12)

        frequency_label = QLabel(
            "Frequency"
        )

        start_label = QLabel(
            "Start Time"
        )

        self._field_label(
            frequency_label
        )

        self._field_label(
            start_label
        )

        self.frequency_combo = QComboBox()

        self.frequency_combo.addItems(
            [
                "Every 2 hours",
                "Every 4 hours",
                "Every 6 hours",
                "Every 8 hours",
                "Every 12 hours",
                "Every 24 hours",
            ]
        )

        self._field_widget(
            self.frequency_combo
        )

        self.start_time = QTimeEdit()

        self.start_time.setDisplayFormat(
            "HH:mm"
        )

        self._field_widget(
            self.start_time
        )

        fields.addWidget(
            frequency_label,
            0,
            0,
        )

        fields.addWidget(
            self.frequency_combo,
            0,
            1,
        )

        fields.addWidget(
            start_label,
            1,
            0,
        )

        fields.addWidget(
            self.start_time,
            1,
            1,
        )

        fields.setColumnStretch(
            0,
            1,
        )

        fields.setColumnStretch(
            1,
            0,
        )

        card_layout.addLayout(
            fields
        )

        schedule_actions = QHBoxLayout()
        schedule_actions.setContentsMargins(
            0,
            4,
            0,
            0,
        )

        self.save_schedule_button = (
            self._flat_button(
                "Save Schedule",
                "#E53935",
            )
        )

        self.save_schedule_button.clicked.connect(
            self._save_schedule
        )

        schedule_actions.addWidget(
            self.save_schedule_button
        )

        schedule_actions.addStretch()

        card_layout.addLayout(
            schedule_actions
        )

        self.schedule_status = QLabel(
            "Scheduled backup is disabled."
        )

        self.schedule_status.setWordWrap(
            True
        )

        self._status_label_style(
            self.schedule_status,
            "#9FA4AE",
            boxed=True,
        )

        card_layout.addWidget(
            self.schedule_status
        )

        card_layout.addStretch()

    # ==========================================================
    # CARD FACTORY
    # ==========================================================

    def _create_card(
        self,
        title,
        accent_color,
    ):

        card = QFrame()
        card.setObjectName(
            "SettingsCard"
        )

        card.setStyleSheet(
            """
            QFrame#SettingsCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            16,
            14,
            16,
            16,
        )

        layout.setSpacing(12)

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:11pt;
                font-weight:700;
                background:transparent;
                border:none;
                padding:0;
            }
            """
        )

        layout.addWidget(
            title_label
        )

        accent = QLabel()
        accent.setFixedHeight(3)

        accent.setStyleSheet(
            f"""
            QLabel {{
                background:{accent_color};
                border:none;
                padding:0;
            }}
            """
        )

        layout.addWidget(
            accent
        )

        card.setMinimumHeight(
            320
        )

        return card

    # ==========================================================
    # COMMON STYLES
    # ==========================================================

    @staticmethod
    def _muted_label(
        label
    ):

        label.setStyleSheet(
            """
            QLabel {
                color:#9FA4AE;
                font-size:9pt;
                background:transparent;
                border:none;
                padding:0;
            }
            """
        )

    @staticmethod
    def _field_label(
        label
    ):

        label.setStyleSheet(
            """
            QLabel {
                color:#F4F5F7;
                font-size:10pt;
                font-weight:600;
                background:transparent;
                border:none;
                padding:0;
            }
            """
        )

    @staticmethod
    def _status_label_style(
        label,
        color,
        boxed=False,
    ):

        if boxed:

            label.setStyleSheet(
                f"""
                QLabel {{
                    color:{color};
                    background:#202226;
                    border:1px solid #34373D;
                    padding:8px 10px;
                    font-size:9pt;
                    font-weight:600;
                }}
                """
            )

        else:

            label.setStyleSheet(
                f"""
                QLabel {{
                    color:{color};
                    background:transparent;
                    border:none;
                    padding:0;
                    font-size:9pt;
                    font-weight:600;
                }}
                """
            )

    @staticmethod
    def _flat_button(
        text,
        color,
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
                color:{color};
                border:none;
                padding:0;
                font-size:10pt;
                font-weight:600;
                text-align:left;
            }}

            QPushButton:hover {{
                color:#FFFFFF;
            }}

            QPushButton:pressed {{
                color:#BFC3CA;
            }}

            QPushButton:disabled {{
                color:#666A71;
            }}
            """
        )

        return button

    @staticmethod
    def _field_widget(
        widget
    ):

        widget.setMinimumHeight(
            36
        )

        widget.setStyleSheet(
            """
            QComboBox,
            QTimeEdit {
                background:#202226;
                color:#F4F5F7;
                border:1px solid #3A3D43;
                padding:0 10px;
                min-width:190px;
            }

            QComboBox:hover,
            QTimeEdit:hover {
                border:1px solid #555A63;
            }

            QComboBox:focus,
            QTimeEdit:focus {
                border:1px solid #29A8FF;
            }

            QComboBox QAbstractItemView {
                background:#202226;
                color:#F4F5F7;
                border:1px solid #3A3D43;
                selection-background-color:#30343B;
            }
            """
        )

    # ==========================================================
    # LOAD SETTINGS
    # ==========================================================

    def _load_settings(self):

        result = (
            self.destination_manager.get_destination()
        )

        if not result["success"]:

            self.destination_input.setText("")

            self._status_label_style(
                self.status_label,
                "#FF5C5C",
            )

            self.status_label.setText(
                "Status: Unable to load destination."
            )

            return

        self.destination_input.setText(
            result["data"][
                "destination_path"
            ]
        )

        self._test_destination(
            show_message=False
        )

    # ==========================================================
    # DESTINATION
    # ==========================================================

    def _browse_destination(self):

        current_path = (
            self.destination_input.text().strip()
        )

        if not current_path:

            current_path = str(
                Path.home()
            )

        selected_directory = (
            QFileDialog.getExistingDirectory(
                self,
                "Select Backup Destination",
                current_path,
                QFileDialog.Option.ShowDirsOnly,
            )
        )

        if not selected_directory:

            return

        self.destination_input.setText(
            selected_directory
        )

        self._test_destination(
            show_message=False
        )

    def _save_destination(self):

        destination_path = (
            self.destination_input.text().strip()
        )

        if not destination_path:

            QMessageBox.warning(
                self,
                "Backup Destination",
                "Please select a backup destination.",
            )

            return

        result = (
            self.destination_manager.set_destination(
                destination_path
            )
        )

        if not result["success"]:

            error_message = (
                result["errors"][0]
                if result["errors"]
                else "Unable to save backup destination."
            )

            self._status_label_style(
                self.status_label,
                "#FF5C5C",
            )

            self.status_label.setText(
                "Status: Destination is not ready."
            )

            QMessageBox.critical(
                self,
                "Backup Destination",
                error_message,
            )

            return

        self.destination_input.setText(
            result["data"][
                "destination_path"
            ]
        )

        self._test_destination(
            show_message=False
        )

        QMessageBox.information(
            self,
            "Backup Destination",
            "Backup destination saved successfully.",
        )

    def _reset_destination(self):

        result = (
            self.destination_manager.reset_destination()
        )

        if not result["success"]:

            error_message = (
                result["errors"][0]
                if result["errors"]
                else "Unable to reset backup destination."
            )

            QMessageBox.critical(
                self,
                "Backup Destination",
                error_message,
            )

            return

        self.destination_input.setText(
            result["data"][
                "destination_path"
            ]
        )

        self._test_destination(
            show_message=False
        )

        QMessageBox.information(
            self,
            "Backup Destination",
            "Backup destination restored to default.",
        )

    def _test_destination(
        self,
        show_message=True,
    ):

        destination_path = (
            self.destination_input.text().strip()
        )

        if not destination_path:

            self._status_label_style(
                self.status_label,
                "#FF9800",
            )

            self.status_label.setText(
                "Status: No destination selected."
            )

            self.storage_label.setText("")

            if show_message:

                QMessageBox.warning(
                    self,
                    "Backup Destination",
                    "Please select a backup destination.",
                )

            return False

        result = (
            self.destination_manager.validate_destination(
                destination_path
            )
        )

        if not result["success"]:

            error_message = (
                result["errors"][0]
                if result["errors"]
                else "Destination validation failed."
            )

            self._status_label_style(
                self.status_label,
                "#FF5C5C",
            )

            self.status_label.setText(
                f"Status: {error_message}"
            )

            self.storage_label.setText("")

            if show_message:

                QMessageBox.warning(
                    self,
                    "Backup Destination",
                    error_message,
                )

            return False

        data = result["data"]

        self._status_label_style(
            self.status_label,
            "#53C653",
        )

        self.status_label.setText(
            "Status: Destination is ready for backup."
        )

        self.storage_label.setText(
            f"Available storage: "
            f"{self._format_bytes(data['free_space'])} "
            f"of {self._format_bytes(data['total_space'])}"
        )

        if show_message:

            QMessageBox.information(
                self,
                "Backup Destination",
                "The backup destination is ready.",
            )

        return True

    # ==========================================================
    # SCHEDULE
    # ==========================================================

    def _save_schedule(self):

        frequency_text = (
            self.frequency_combo.currentText()
        )

        frequency_hours = int(
            frequency_text.split()[1]
        )

        start_time = (
            self.start_time
            .time()
            .toString("HH:mm")
        )

        enabled = (
            self.schedule_enabled.isChecked()
        )

        if enabled and not self._test_destination(
            show_message=False
        ):

            QMessageBox.warning(
                self,
                "Scheduled Backup",
                (
                    "Please configure a valid backup destination "
                    "before enabling Scheduled Backup."
                ),
            )

            self.schedule_enabled.setChecked(
                False
            )

            return

        self.scheduler.configure(
            enabled=enabled,
            frequency_hours=frequency_hours,
            start_time=start_time,
        )

        self._update_schedule_status()

        QMessageBox.information(
            self,
            "Scheduled Backup",
            "Scheduled backup settings saved successfully.",
        )

    def _load_schedule(self):

        self.schedule_enabled.setChecked(
            self.scheduler.is_enabled()
        )

        hours = (
            self.scheduler.get_frequency_hours()
        )

        mapping = {
            2: 0,
            4: 1,
            6: 2,
            8: 3,
            12: 4,
            24: 5,
        }

        self.frequency_combo.setCurrentIndex(
            mapping.get(
                hours,
                2,
            )
        )

        start_time = (
            self.scheduler.get_start_time()
        )

        try:

            hour, minute = map(
                int,
                start_time.split(":"),
            )

            self.start_time.setTime(
                QTime(
                    hour,
                    minute,
                )
            )

        except Exception:

            pass

        self._update_schedule_status()

    def _update_schedule_status(self):

        if not self.scheduler.is_enabled():

            self._status_label_style(
                self.schedule_status,
                "#9FA4AE",
                boxed=True,
            )

            self.schedule_status.setText(
                "Scheduled backup is disabled."
            )

            return

        next_backup = (
            self.scheduler.get_next_backup()
        )

        frequency = (
            self.scheduler.get_frequency_hours()
        )

        if next_backup:

            next_text = (
                next_backup.strftime(
                    "%d/%m/%Y  %H:%M"
                )
            )

            self.schedule_status.setText(
                f"Scheduled backup active  β€Ά  "
                f"Every {frequency} hours  β€Ά  "
                f"Next backup: {next_text}"
            )

        else:

            self.schedule_status.setText(
                f"Scheduled backup active  β€Ά  "
                f"Every {frequency} hours"
            )

        self._status_label_style(
            self.schedule_status,
            "#53C653",
            boxed=True,
        )

    def _scheduled_backup_started(self):

        self.schedule_status.setText(
            "Scheduled backup started."
        )

        self._status_label_style(
            self.schedule_status,
            "#29A8FF",
            boxed=True,
        )

    # ==========================================================
    # FORMAT
    # ==========================================================

    @staticmethod
    def _format_bytes(
        value,
    ):

        value = float(value)

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
        ]

        for unit in units:

            if value < 1024:

                return (
                    f"{value:.1f} {unit}"
                )

            value /= 1024

        return (
            f"{value:.1f} PB"
        )

