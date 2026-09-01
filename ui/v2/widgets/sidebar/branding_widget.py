from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from core.common.resource_path import resource_path


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
        # JV Toolbox logo
        #

        self.logo = QLabel()

        self.logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.logo.setFixedSize(
            120,
            120,
        )

        self.logo.setStyleSheet(
            """
            QLabel {
                background: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }
            """
        )

        logo_path = resource_path(
            "assets/branding/logo/logo.png"
        )

        pixmap = QPixmap(
            logo_path
        )

        if not pixmap.isNull():

            pixmap = pixmap.scaled(
                120,
                120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.logo.setPixmap(
                pixmap
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
            "JV Toolbox"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title.setStyleSheet(
            """
            QLabel {
                background: transparent;
                border: none;
                color: #F5F7FA;
                font-size: 12pt;
                font-weight: 700;
                padding: 0;
                margin: 0;
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