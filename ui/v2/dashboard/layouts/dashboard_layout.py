from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)

from ui.v2.widgets.header.header import Header
from ui.v2.widgets.footer.footer import Footer

from ui.v2.dashboard.sections.summary_section import SummarySection
from ui.v2.dashboard.sections.operations_section import OperationsSection


class DashboardLayout(QWidget):

    def __init__(self):

        super().__init__()

        self.setObjectName(
            "DashboardLayout"
        )

        self.setStyleSheet(
            """
            QWidget#DashboardLayout {
                background: transparent;
                border: none;
            }

            QLabel#DashboardTitle {
                background: transparent;
                border: none;
                color: #F5F7FA;
                font-size: 26pt;
                font-weight: 700;
                padding: 0;
                margin: 0;
            }

            QLabel#DashboardSubtitle {
                background: transparent;
                border: none;
                color: #98A3B3;
                font-size: 10.5pt;
                font-weight: 400;
                padding: 0;
                margin: 0;
            }
            """
        )

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            22,
            18,
            22,
            16,
        )

        layout.setSpacing(
            14
        )

        #
        # PAGE HEADER
        #

        top_row = QHBoxLayout()

        top_row.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        top_row.setSpacing(
            18
        )

        #
        # TITLE COLUMN
        #

        title_column = QVBoxLayout()

        title_column.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        title_column.setSpacing(
            2
        )

        #
        # Dashboard title
        #

        title = QLabel(
            "Dashboard"
        )

        title.setObjectName(
            "DashboardTitle"
        )

        #
        # Subtitle
        #

        subtitle = QLabel(
            "Monitor your backup activity and system status"
        )

        subtitle.setObjectName(
            "DashboardSubtitle"
        )

        title_column.addWidget(
            title
        )

        title_column.addWidget(
            subtitle
        )

        top_row.addLayout(
            title_column,
            1,
        )

        #
        # HEADER / UDL
        #

        self.header = Header()

        top_row.addWidget(
            self.header,
            0,
            Qt.AlignmentFlag.AlignBottom,
        )

        layout.addLayout(
            top_row
        )

        #
        # DASHBOARD CONTENT
        #

        self.summary = SummarySection()

        self.operations = OperationsSection()

        self.footer = Footer()

        layout.addWidget(
            self.summary
        )

        layout.addWidget(
            self.operations,
            1,
        )

        layout.addWidget(
            self.footer
        )

        self.setLayout(
            layout
        )