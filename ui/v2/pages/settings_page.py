from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QFrame,
)

from ui.v2.styles.theme import Theme

from core.destination_manager import (
    DestinationManager,
)


class SettingsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.destination_manager = (
            DestinationManager()
        )

        self._build_ui()

        self._load_settings()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        layout.setSpacing(16)

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        title = QLabel(
            "Settings"
        )

        title.setFont(
            Theme.Typography.title()
        )

        title.setStyleSheet(
            f"""
            color: {Theme.Colors.TEXT};
            """
        )

        layout.addWidget(
            title
        )

        # -----------------------------------------------------
        # Backup Destination Card
        # -----------------------------------------------------

        card = QFrame()

        card.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
            }}
            """
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

        card_layout.setSpacing(12)

        # -----------------------------------------------------
        # Section title
        # -----------------------------------------------------

        destination_title = QLabel(
            "Backup Destination"
        )

        destination_title.setStyleSheet(
            f"""
            color: {Theme.Colors.TEXT};
            font-size: 17px;
            font-weight: 600;
            border: none;
            """
        )

        card_layout.addWidget(
            destination_title
        )

        # -----------------------------------------------------
        # Description
        # -----------------------------------------------------

        description = QLabel(
            "Select where backup files will be stored."
        )

        description.setWordWrap(
            True
        )

        description.setStyleSheet(
            f"""
            color: #6b7280;
            font-size: 13px;
            border: none;
            """
        )

        card_layout.addWidget(
            description
        )

        # -----------------------------------------------------
        # Destination input
        # -----------------------------------------------------

        destination_row = QHBoxLayout()

        destination_row.setSpacing(
            8
        )

        self.destination_input = (
            QLineEdit()
        )

        self.destination_input.setReadOnly(
            True
        )

        self.destination_input.setMinimumHeight(
            38
        )

        self.destination_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #f9fafb;
                border: 1px solid #d1d5db;
                border-radius: 7px;
                padding: 0 10px;
                color: #111827;
            }
            """
        )

        destination_row.addWidget(
            self.destination_input
        )

        self.browse_button = QPushButton(
            "Browse..."
        )

        self.browse_button.setMinimumHeight(
            38
        )

        self.browse_button.setMinimumWidth(
            100
        )

        self.browse_button.clicked.connect(
            self._browse_destination
        )

        destination_row.addWidget(
            self.browse_button
        )

        card_layout.addLayout(
            destination_row
        )

        # -----------------------------------------------------
        # Action buttons
        # -----------------------------------------------------

        actions_row = QHBoxLayout()

        actions_row.setSpacing(
            8
        )

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.setMinimumHeight(
            36
        )

        self.save_button.clicked.connect(
            self._save_destination
        )

        actions_row.addWidget(
            self.save_button
        )

        self.test_button = QPushButton(
            "Test Destination"
        )

        self.test_button.setMinimumHeight(
            36
        )

        self.test_button.clicked.connect(
            self._test_destination
        )

        actions_row.addWidget(
            self.test_button
        )

        self.reset_button = QPushButton(
            "Reset to Default"
        )

        self.reset_button.setMinimumHeight(
            36
        )

        self.reset_button.clicked.connect(
            self._reset_destination
        )

        actions_row.addWidget(
            self.reset_button
        )

        actions_row.addStretch()

        card_layout.addLayout(
            actions_row
        )

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        self.status_label = QLabel(
            "Status: Unknown"
        )

        self.status_label.setWordWrap(
            True
        )

        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #6b7280;
                font-size: 13px;
                border: none;
                padding-top: 4px;
            }
            """
        )

        card_layout.addWidget(
            self.status_label
        )

        # -----------------------------------------------------
        # Storage information
        # -----------------------------------------------------

        self.storage_label = QLabel(
            ""
        )

        self.storage_label.setWordWrap(
            True
        )

        self.storage_label.setStyleSheet(
            """
            QLabel {
                color: #6b7280;
                font-size: 12px;
                border: none;
            }
            """
        )

        card_layout.addWidget(
            self.storage_label
        )

        layout.addWidget(
            card
        )

        layout.addStretch()

    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    def _load_settings(self):

        result = (
            self.destination_manager
            .get_destination()
        )

        if not result["success"]:

            self.destination_input.setText(
                ""
            )

            self.status_label.setText(
                "Status: Unable to load destination."
            )

            return

        destination_path = (
            result["data"][
                "destination_path"
            ]
        )

        self.destination_input.setText(
            destination_path
        )

        self._test_destination(
            show_message=False
        )

    # ---------------------------------------------------------
    # Browse
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

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
            self.destination_manager
            .set_destination(
                destination_path
            )
        )

        if not result["success"]:

            error_message = (
                result["errors"][0]
                if result["errors"]
                else "Unable to save backup destination."
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

        self.status_label.setText(
            "Status: ✓ Backup destination saved and ready."
        )

        self._test_destination(
            show_message=False
        )

        QMessageBox.information(
            self,
            "Backup Destination",
            "Backup destination saved successfully.",
        )

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def _reset_destination(self):

        result = (
            self.destination_manager
            .reset_destination()
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

        destination_path = (
            result["data"][
                "destination_path"
            ]
        )

        self.destination_input.setText(
            destination_path
        )

        self._test_destination(
            show_message=False
        )

        QMessageBox.information(
            self,
            "Backup Destination",
            "Backup destination restored to default.",
        )

    # ---------------------------------------------------------
    # Test
    # ---------------------------------------------------------

    def _test_destination(
        self,
        show_message=True,
    ):

        destination_path = (
            self.destination_input.text().strip()
        )

        if not destination_path:

            self.status_label.setText(
                "Status: ✗ No destination selected."
            )

            self.storage_label.setText(
                ""
            )

            if show_message:

                QMessageBox.warning(
                    self,
                    "Backup Destination",
                    "Please select a backup destination.",
                )

            return False

        result = (
            self.destination_manager
            .validate_destination(
                destination_path
            )
        )

        if not result["success"]:

            error_message = (
                result["errors"][0]
                if result["errors"]
                else "Destination validation failed."
            )

            self.status_label.setText(
                f"Status: ✗ {error_message}"
            )

            self.status_label.setStyleSheet(
                """
                QLabel {
                    color: #dc2626;
                    font-size: 13px;
                    border: none;
                    padding-top: 4px;
                }
                """
            )

            self.storage_label.setText(
                ""
            )

            if show_message:

                QMessageBox.warning(
                    self,
                    "Backup Destination",
                    error_message,
                )

            return False

        data = result["data"]

        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #16a34a;
                font-size: 13px;
                border: none;
                padding-top: 4px;
            }
            """
        )

        self.status_label.setText(
            "Status: ✓ Destination is ready for backup."
        )

        free_space = (
            self._format_bytes(
                data["free_space"]
            )
        )

        total_space = (
            self._format_bytes(
                data["total_space"]
            )
        )

        self.storage_label.setText(
            f"Available storage: {free_space} "
            f"of {total_space}"
        )

        if show_message:

            QMessageBox.information(
                self,
                "Backup Destination",
                "The backup destination is ready.",
            )

        return True

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _format_bytes(
        value,
    ):

        value = float(
            value
        )

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