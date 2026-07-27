from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
)

from ui.v2.styles.theme import Theme


class StatusWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(
            f"""
            color: {Theme.Colors.BORDER};
            background: {Theme.Colors.BORDER};
            max-height:1px;
            """
        )

        title = QLabel("SYSTEM STATUS")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title.setStyleSheet(f"""
            QLabel {{
                color: {Theme.Colors.TEXT_DISABLED};
                font-size:9pt;
                font-weight:600;
                letter-spacing:1px;
                background:transparent;
            }}
        """)

        self.status = QLabel("🟢 READY")
        self.status.setStyleSheet(f"""
            QLabel {{
                color:{Theme.Colors.SUCCESS};
                font-size:13pt;
                font-weight:700;
                background:transparent;
            }}
        """)

        version_title = QLabel("VERSION")
        version_title.setStyleSheet(f"""
            QLabel {{
                color:{Theme.Colors.TEXT_DISABLED};
                font-size:9pt;
                background:transparent;
            }}
        """)

        version = QLabel("v2.0.0")
        version.setStyleSheet(f"""
            QLabel {{
                color:{Theme.Colors.TEXT};
                font-size:11pt;
                font-weight:600;
                background:transparent;
            }}
        """)

        layout.addWidget(separator)
        layout.addSpacing(8)
        layout.addWidget(title)
        layout.addWidget(self.status)
        layout.addSpacing(12)
        layout.addWidget(version_title)
        layout.addWidget(version)