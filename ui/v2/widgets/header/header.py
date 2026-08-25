from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QDialog,
)

from ui.v2.widgets.header.database_selector import DatabaseSelector
from core.database.database_context import database_context


class Header(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.update_database_display(
            database_context.active()
        )

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        self.setFixedHeight(
            48
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            12
        )

        # ======================================================
        # RIGHT SIDE
        # ======================================================

        right = QHBoxLayout()

        right.setContentsMargins(
            0,
            0,
            0,
            0
        )

        right.setSpacing(
            12
        )

        # ======================================================
        # CONNECTION STATUS
        #
        # ONLY an indicator.
        # It does NOT open anything.
        # ======================================================

        self.connected = QLabel(
            "Not Connected"
        )

        self.connected.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.connected.setMinimumWidth(
            110
        )

        self.connected.setFixedHeight(
            32
        )

        self.connected.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#FF9800;
                padding:0;
                margin:0;
                font-size:9pt;
                font-weight:700;
            }
            """
        )

        # ======================================================
        # GEAR
        #
        # Opens Select Database
        # ======================================================

        self.settings_button = QPushButton()

        self.settings_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.settings_button.setFixedSize(
            36,
            36
        )

        self.settings_button.setFlat(
            True
        )

        self.settings_button.setIcon(
            QIcon(
                "assets/icons/navigation/settings.svg"
            )
        )

        self.settings_button.setIconSize(
            QSize(
                24,
                24
            )
        )

        self.settings_button.setToolTip(
            "Select Database"
        )

        self.settings_button.setStyleSheet(
            """
            QPushButton {
                background:transparent;
                border:none;
                padding:0;
                margin:0;
            }

            QPushButton:hover {
                background:transparent;
                border:none;
            }

            QPushButton:pressed {
                background:transparent;
                border:none;
            }
            """
        )

        self.settings_button.clicked.connect(
            self.open_database_selector
        )

        # ======================================================
        # ADD
        # ======================================================

        right.addWidget(
            self.connected
        )

        right.addWidget(
            self.settings_button
        )

        layout.addStretch()

        layout.addLayout(
            right
        )

        # ======================================================
        # DATABASE CHANGE
        # ======================================================

        database_context.database_changed.connect(
            self.update_database_display
        )

    # ==========================================================
    # DATABASE SELECTOR
    # ==========================================================

    def open_database_selector(
        self
    ):

        dialog = DatabaseSelector(
            self
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):

            return

        if not dialog.selected_udl:

            return

        database_context.select(
            dialog.selected_udl
        )

    # ==========================================================
    # DATABASE DISPLAY
    # ==========================================================

    def update_database_display(
        self,
        database
    ):

        if not database:

            self.connected.setText(
                "Not Connected"
            )

            self.connected.setStyleSheet(
                """
                QLabel {
                    background:transparent;
                    border:none;
                    color:#FF9800;
                    padding:0;
                    margin:0;
                    font-size:9pt;
                    font-weight:700;
                }
                """
            )

            return

        self.connected.setText(
            "Connected"
        )

        self.connected.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#53C653;
                padding:0;
                margin:0;
                font-size:9pt;
                font-weight:700;
            }
            """
        )