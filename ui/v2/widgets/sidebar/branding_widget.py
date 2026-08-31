from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from ui.v2.widgets.common.svg_icon import SvgIcon


class BrandingWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            20,
            0,
            20,
        )

        layout.setSpacing(
            10
        )

        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        #
        # Support Agent logo
        #

        self.logo = SvgIcon(
            "support_agent.svg",
            size=120,
        )

        layout.addWidget(
            self.logo,
            0,
            Qt.AlignmentFlag.AlignHCenter,
        )

        #
        # Product name
        #

        self.title = QLabel(
            "Sunsoft Support Agent"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title.setStyleSheet(
            """
            QLabel {
                background:transparent;
                border:none;
                color:#F5F7FA;
                font-size:12pt;
                font-weight:700;
                padding:0;
                margin:0;
            }
            """
        )

        self.title.setWordWrap(
            True
        )

        layout.addWidget(
            self.title
        )

        layout.addStretch()
