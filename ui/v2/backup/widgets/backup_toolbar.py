from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
)

from ui.v2.styles.theme import Theme


class BackupToolbar(QWidget):

    start_backup = Signal()
    cancel_backup = Signal()
    browse_clicked = Signal()
    open_destination_clicked = Signal()

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.setObjectName(
            "BackupToolbar"
        )

        self.setStyleSheet(
            f"""
            QWidget#BackupToolbar {{
                background:{Theme.Colors.SURFACE};
                border:1px solid {Theme.Colors.BORDER};
                border-radius:12px;
            }}

            QLabel {{
                background:transparent;
                border:none;
            }}

            QPushButton {{
                background:transparent;
                border:none;
                border-radius:0px;
                color:{Theme.Colors.TEXT};
                min-height:40px;
                padding:0 12px;
                font-size:10pt;
                font-weight:600;
            }}

            QPushButton:hover {{
                background:#292b30;
                color:#ffffff;
            }}

            QPushButton:pressed {{
                background:#34363b;
            }}

            QPushButton#startButton {{
                color:#ef4444;
            }}

            QPushButton#startButton:hover {{
                background:#302529;
                color:#ff6666;
            }}

            QPushButton#cancelButton {{
                color:#ff9800;
            }}

            QPushButton#cancelButton:hover {{
                background:#302c24;
                color:#ffb74d;
            }}

            QPushButton#cancelButton:disabled {{
                color:#555a61;
                background:transparent;
            }}

            QPushButton#secondaryButton {{
                color:{Theme.Colors.TEXT};
            }}

            QPushButton#secondaryButton:hover {{
                background:#292b30;
                color:#ffffff;
            }}
            """
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            14,
            8,
            14,
            8
        )

        layout.setSpacing(
            2
        )

        title = QLabel(
            "Backup Actions"
        )

        title.setStyleSheet(
            f"""
            QLabel {{
                background:transparent;
                border:none;
                color:{Theme.Colors.TEXT};
                font-size:10pt;
                font-weight:700;
                padding:0 8px;
            }}
            """
        )

        layout.addWidget(
            title
        )

        layout.addStretch()

        # ======================================================
        # START
        # ======================================================

        self.start_button = QPushButton(
            "▶  Start Backup"
        )

        self.start_button.setObjectName(
            "startButton"
        )

        self.start_button.setCursor(
            __import__("PySide6.QtCore", fromlist=["Qt"]).Qt.PointingHandCursor
        )

        self.start_button.clicked.connect(
            self.start_backup.emit
        )

        # ======================================================
        # CANCEL
        # ======================================================

        self.cancel_button = QPushButton(
            "■  Cancel Backup"
        )

        self.cancel_button.setObjectName(
            "cancelButton"
        )

        self.cancel_button.setCursor(
            __import__("PySide6.QtCore", fromlist=["Qt"]).Qt.PointingHandCursor
        )

        self.cancel_button.setEnabled(
            False
        )

        self.cancel_button.clicked.connect(
            self.cancel_backup.emit
        )

        # ======================================================
        # BROWSE
        # ======================================================

        self.browse_button = QPushButton(
            "📁  Browse"
        )

        self.browse_button.setObjectName(
            "secondaryButton"
        )

        self.browse_button.setCursor(
            __import__("PySide6.QtCore", fromlist=["Qt"]).Qt.PointingHandCursor
        )

        self.browse_button.clicked.connect(
            self.browse_clicked.emit
        )

        # ======================================================
        # OPEN FOLDER
        # ======================================================

        self.open_button = QPushButton(
            "📂  Open Folder"
        )

        self.open_button.setObjectName(
            "secondaryButton"
        )

        self.open_button.setCursor(
            __import__("PySide6.QtCore", fromlist=["Qt"]).Qt.PointingHandCursor
        )

        self.open_button.clicked.connect(
            self.open_destination_clicked.emit
        )

        layout.addWidget(
            self.start_button
        )

        layout.addWidget(
            self.cancel_button
        )

        layout.addWidget(
            self.browse_button
        )

        layout.addWidget(
            self.open_button
        )

    def set_backup_running(
        self,
        running: bool
    ):

        self.start_button.setEnabled(
            not running
        )

        self.cancel_button.setEnabled(
            running
        )