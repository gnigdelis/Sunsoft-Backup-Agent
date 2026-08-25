from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QPushButton,
    QFrame,
    QMessageBox,
    QScrollArea,
)

from core.database.database_context import database_context

from core.maintenance.extra_lock_service import (
    extra_lock_service,
)


class ExtraLockPage(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.spinboxes = []

        self.setup_ui()

        database_context.database_changed.connect(
            self.on_database_changed
        )

        self.load_values()

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        main_layout.setSpacing(
            14
        )

        # ======================================================
        # EXTRA LOCK CARD
        # ======================================================

        card = QFrame()

        card.setObjectName(
            "ExtraLockCard"
        )

        card.setStyleSheet(
            """
            QFrame#ExtraLockCard {
                background:#25262B;
                border:1px solid #393C43;
            }
            """
        )

        card_layout = QVBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            16,
            14,
            16,
            16,
        )

        card_layout.setSpacing(
            12
        )

        # ======================================================
        # TITLE
        # ======================================================

        title = QLabel(
            "Extra Lock"
        )

        title.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#F5F7FA;
                font-size:11pt;
                font-weight:700;
                padding:0;
                margin:0;
            }
            """
        )

        card_layout.addWidget(
            title
        )

        # ======================================================
        # ACCENT
        # ======================================================

        accent = QLabel()

        accent.setFixedHeight(
            3
        )

        accent.setStyleSheet(
            """
            QLabel {
                background:#AB47BC;
                border:none;
            }
            """
        )

        card_layout.addWidget(
            accent
        )

        # ======================================================
        # DESCRIPTION
        # ======================================================

        description = QLabel(
            "View and manage the active Extra Lock settings for the selected database."
        )

        description.setWordWrap(
            True
        )

        description.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#98A3B3;
                font-size:9pt;
                padding:0;
                margin:0;
            }
            """
        )

        card_layout.addWidget(
            description
        )

        # ======================================================
        # DATABASE INFORMATION
        # ======================================================

        database_info = QHBoxLayout()

        database_info.setContentsMargins(
            0,
            0,
            0,
            0
        )

        database_caption = QLabel(
            "Database"
        )

        database_caption.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#98A3B3;
                font-size:9pt;
            }
            """
        )

        self.database_label = QLabel(
            "Not selected"
        )

        self.database_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        self.database_label.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#F5F7FA;
                font-size:9pt;
                font-weight:700;
            }
            """
        )

        database_info.addWidget(
            database_caption
        )

        database_info.addStretch()

        database_info.addWidget(
            self.database_label
        )

        card_layout.addLayout(
            database_info
        )

        # ======================================================
        # OPTIONS TITLE
        # ======================================================

        options_title = QLabel(
            "Active Extra Lock Options"
        )

        options_title.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#F4F5F7;
                font-size:10pt;
                font-weight:700;
            }
            """
        )

        card_layout.addWidget(
            options_title
        )

        # ======================================================
        # SCROLL AREA
        # ======================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        scroll.setStyleSheet(
            """
            QScrollArea {
                background:transparent;
                border:none;
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

        content = QWidget()

        content.setStyleSheet(
            """
            QWidget {
                background:transparent;
                border:none;
            }
            """
        )

        self.items_layout = QVBoxLayout(
            content
        )

        self.items_layout.setContentsMargins(
            0,
            2,
            0,
            2
        )

        self.items_layout.setSpacing(
            6
        )

        scroll.setWidget(
            content
        )

        card_layout.addWidget(
            scroll,
            1
        )

        # ======================================================
        # BUTTONS
        # ======================================================

        buttons_layout = QHBoxLayout()

        buttons_layout.setContentsMargins(
            0,
            4,
            0,
            0
        )

        buttons_layout.setSpacing(
            12
        )

        self.reload_button = QPushButton(
            "↻  Refresh"
        )

        self.save_button = QPushButton(
            "▶  Save Changes"
        )

        self.reload_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.save_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.reload_button.setMinimumHeight(
            36
        )

        self.save_button.setMinimumHeight(
            36
        )

        self.reload_button.setStyleSheet(
            """
            QPushButton {
                background:transparent;
                border:none;
                color:#29A8FF;
                font-size:9pt;
                font-weight:600;
                padding:0;
            }

            QPushButton:hover {
                color:#65C5FF;
            }

            QPushButton:pressed {
                color:#1688D3;
            }

            QPushButton:disabled {
                color:#59616B;
            }
            """
        )

        self.save_button.setStyleSheet(
            """
            QPushButton {
                background:transparent;
                border:none;
                color:#E53935;
                font-size:9pt;
                font-weight:600;
                padding:0;
            }

            QPushButton:hover {
                color:#FF5A56;
            }

            QPushButton:pressed {
                color:#C62828;
            }

            QPushButton:disabled {
                color:#59616B;
            }
            """
        )

        self.reload_button.clicked.connect(
            self.load_values
        )

        self.save_button.clicked.connect(
            self.save_values
        )

        buttons_layout.addWidget(
            self.reload_button
        )

        buttons_layout.addStretch()

        buttons_layout.addWidget(
            self.save_button
        )

        card_layout.addLayout(
            buttons_layout
        )

        main_layout.addWidget(
            card,
            1
        )

    # ==========================================================
    # DATABASE
    # ==========================================================

    def on_database_changed(
        self,
        database,
    ):

        if not database:

            self.database_label.setText(
                "Not selected"
            )

            self.clear_items()

            return

        self.database_label.setText(
            database.get(
                "name",
                "Unknown"
            )
        )

        self.load_values()

    # ==========================================================
    # HELPERS
    # ==========================================================

    def clear_items(
        self
    ):

        self.spinboxes.clear()

        while self.items_layout.count():

            item = self.items_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

    # ==========================================================
    # LOAD
    # ==========================================================

    def load_values(
        self
    ):

        self.clear_items()

        database = (
            database_context.active()
        )

        if not database:

            self.database_label.setText(
                "Not selected"
            )

            self.set_controls_enabled(
                False
            )

            return

        self.database_label.setText(
            database.get(
                "name",
                "Unknown"
            )
        )

        try:

            result = (
                extra_lock_service.load()
            )

            for item in result["items"]:

                row = QFrame()

                row.setObjectName(
                    "ExtraLockRow"
                )

                row.setStyleSheet(
                    """
                    QFrame#ExtraLockRow {
                        background:#202226;
                        border:1px solid #34373D;
                    }

                    QFrame#ExtraLockRow:hover {
                        border:1px solid #454A52;
                    }
                    """
                )

                row_layout = QHBoxLayout(
                    row
                )

                row_layout.setContentsMargins(
                    12,
                    7,
                    10,
                    7
                )

                row_layout.setSpacing(
                    10
                )

                name_label = QLabel(
                    item.name
                )

                name_label.setMinimumWidth(
                    180
                )

                name_label.setStyleSheet(
                    """
                    QLabel {
                        background:transparent;
                        border:none;
                        color:#D9DCE2;
                        font-size:9pt;
                        font-weight:600;
                    }
                    """
                )

                value = QSpinBox()

                value.setMinimum(
                    0
                )

                value.setMaximum(
                    999
                )

                value.setValue(
                    item.value
                )

                value.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                value.setMinimumWidth(
                    82
                )

                value.setFixedHeight(
                    28
                )

                value.setStyleSheet(
                    """
                    QSpinBox {
                        background:#25262B;
                        color:#F4F5F7;
                        border:1px solid #393C43;
                        padding:2px 6px;
                        font-size:9pt;
                    }

                    QSpinBox:hover {
                        border:1px solid #555A63;
                    }

                    QSpinBox:focus {
                        border:1px solid #AB47BC;
                    }

                    QSpinBox::up-button,
                    QSpinBox::down-button {
                        background:#2B2D33;
                        border:none;
                        width:18px;
                    }
                    """
                )

                row_layout.addWidget(
                    name_label
                )

                row_layout.addStretch()

                row_layout.addWidget(
                    value
                )

                self.items_layout.addWidget(
                    row
                )

                self.spinboxes.append(
                    value
                )

            self.items_layout.addStretch()

            self.set_controls_enabled(
                True
            )

        except Exception as exc:

            self.set_controls_enabled(
                False
            )

            QMessageBox.critical(
                self,
                "Extra Lock",
                f"Unable to load Extra Lock settings:\n\n{exc}",
            )

    # ==========================================================
    # SAVE
    # ==========================================================

    def save_values(
        self
    ):

        if not database_context.is_selected():

            QMessageBox.warning(
                self,
                "Extra Lock",
                "No database is selected.",
            )

            return

        values = [
            spinbox.value()
            for spinbox in self.spinboxes
        ]

        confirmation = QMessageBox.question(
            self,
            "Confirm Changes",
            "Save the changes to the Extra Lock settings?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if (
            confirmation
            != QMessageBox.StandardButton.Yes
        ):

            return

        self.set_controls_enabled(
            False
        )

        try:

            result = (
                extra_lock_service.save(
                    values
                )
            )

            QMessageBox.information(
                self,
                "Extra Lock",
                "The changes were saved successfully.",
            )

            self.load_values()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Extra Lock",
                f"Saving failed:\n\n{exc}",
            )

            self.set_controls_enabled(
                True
            )

    # ==========================================================
    # CONTROLS
    # ==========================================================

    def set_controls_enabled(
        self,
        enabled,
    ):

        self.reload_button.setEnabled(
            enabled
        )

        self.save_button.setEnabled(
            enabled
        )

        for spinbox in self.spinboxes:

            spinbox.setEnabled(
                enabled
            )