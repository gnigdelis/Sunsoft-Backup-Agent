from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from ui.v2.pages.database_maintenance.extra_lock_page import (
    ExtraLockPage,
)


class HistoryPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            18,
            20,
            22,
        )

        layout.setSpacing(
            14
        )

        # ======================================================
        # HEADER
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
                font-size:26pt;
                font-weight:700;
                padding:0;
                margin:0;
            }
            """
        )

        subtitle = QLabel(
            "View and manage the active Extra Lock settings"
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

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        # ======================================================
        # EXTRA LOCK
        # ======================================================

        self.extra_lock_page = ExtraLockPage(
            self
        )

        layout.addWidget(
            self.extra_lock_page,
            1
        )

        self.setLayout(
            layout
        )