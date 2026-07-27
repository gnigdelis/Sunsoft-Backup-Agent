from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
)

from ui.v2.styles.theme import Theme
from ui.v2.widgets.common.status_chip import StatusChip


class Header(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        self.setFixedHeight(48)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        #
        # LEFT
        #

        status = QLabel("Everything is running normally.")

        status.setStyleSheet(f"""
            QLabel {{
                color:#53C653;
                font-size:11pt;
                font-weight:600;
                background:transparent;
            }}
        """)

        #
        # RIGHT
        #

        right = QHBoxLayout()
        right.setSpacing(12)

        connected = StatusChip(
            "Connected",
            "success",
        )

        settings = QPushButton("⚙")

        settings.setCursor(Qt.PointingHandCursor)
        settings.setFixedSize(42, 42)

        settings.setStyleSheet(f"""
            QPushButton {{
                background:{Theme.Colors.PRIMARY};
                color:white;
                border:none;
                border-radius:10px;
                font-size:13pt;
                font-weight:bold;
            }}

            QPushButton:hover {{
                background:#ff4b4b;
            }}
        """)

        right.addWidget(connected)
        right.addWidget(settings)

        layout.addWidget(status)

        layout.addStretch()

        layout.addLayout(right)