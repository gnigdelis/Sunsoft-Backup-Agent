from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from ui.v2.styles.theme import Theme


class BrandingWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # --------------------------------------------------
        # Logo
        # --------------------------------------------------

        self.logo = QLabel()
        self.logo.setFixedSize(96, 96)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap("assets/icons/logo.png")

        if not pixmap.isNull():
            self.logo.setPixmap(
                pixmap.scaled(
                    88,
                    88,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            self.logo.setText("🛡")
            self.logo.setStyleSheet("font-size:64px;")

        # --------------------------------------------------
        # Brand
        # --------------------------------------------------

        self.company = QLabel("SUNSOFT")
        self.company.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.product = QLabel("Support Agent")
        self.product.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tagline = QLabel("Support & Backup Suite")
        self.tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.company.setStyleSheet(f"""
            QLabel {{
                color:{Theme.Colors.PRIMARY};
                font-size:20px;
                font-weight:800;
                letter-spacing:2px;
                background:transparent;
            }}
        """)

        self.product.setStyleSheet(f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:18px;
                font-weight:700;
                background:transparent;
            }}
        """)

        self.tagline.setStyleSheet(f"""
            QLabel {{
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:11px;
                background:transparent;
            }}
        """)

        layout.addWidget(self.logo)
        layout.addWidget(self.company)
        layout.addWidget(self.product)
        layout.addWidget(self.tagline)