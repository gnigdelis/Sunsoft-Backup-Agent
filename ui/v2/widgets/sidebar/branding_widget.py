from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

from ui.v2.widgets.common.svg_icon import SvgIcon


class BrandingWidget(QWidget):

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
            8,
            10,
            8,
            8,
        )

        layout.setSpacing(
            8
        )

        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
            | Qt.AlignmentFlag.AlignHCenter
        )

        #
        # Support Agent Logo
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
        # Product Name
        #

        self.product = QLabel(
            "Support Αgent"
        )

        self.product.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.product.setStyleSheet(
            """
            QLabel {
                background: transparent;
                color: #F5F7FA;
                font-size: 18px;
                font-weight: 700;
                border: none;
            }
            """
        )

        layout.addWidget(
            self.product
        )

        self.setLayout(
            layout
        )