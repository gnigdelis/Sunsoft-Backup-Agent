from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from core.assets.asset_manager import AssetManager
from ui.v2.styles.theme import Theme


class BrandingWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            18,
            14,
            18,
            14,
        )

        layout.setSpacing(0)

        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
            | Qt.AlignmentFlag.AlignHCenter
        )

        #
        # Logo
        #

        self.logo = QLabel()

        self.logo.setFixedSize(
            128,
            128,
        )

        self.logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        pixmap = QPixmap(
            AssetManager.branding(
                "logo",
                "logo.png",
            )
        )

        if not pixmap.isNull():

            self.logo.setPixmap(
                pixmap.scaled(
                    120,
                    120,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        else:

            self.logo.setText("SS")

            self.logo.setStyleSheet(
                f"""
                color:{Theme.Colors.PRIMARY};
                font-size:42px;
                font-weight:800;
                """
            )

        #
        # Product
        #

        self.product = QLabel("Support Agent")

        self.product.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.product.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:20px;
            font-weight:700;
            """
        )

        #
        # Tagline
        #

        self.tagline = QLabel(
            "Enterprise Backup Suite"
        )

        self.tagline.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.tagline.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:11px;
            """
        )

        layout.addWidget(self.logo)
        layout.addSpacing(6)
        layout.addWidget(self.product)
        layout.addSpacing(2)
        layout.addWidget(self.tagline)