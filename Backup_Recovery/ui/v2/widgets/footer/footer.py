from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)

from ui.v2.styles.theme import Theme


class Footer(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        self.setFixedHeight(42)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(18)

        self.setStyleSheet(f"""
            QWidget {{
                background:transparent;
                border-top:1px solid {Theme.Colors.BORDER};
            }}

            QLabel {{
                background:transparent;
                color:{Theme.Colors.TEXT_SECONDARY};
                font-size:9pt;
            }}
        """)

        app = QLabel("Sunsoft Support Agent v2.0")

        engine = QLabel("Engine : Ready")

        database = QLabel("Database : Connected")

        provider = QLabel("Provider : Idle")

        version = QLabel("Build 2.0.0")

        layout.addWidget(app)
        layout.addSpacing(20)
        layout.addWidget(engine)
        layout.addSpacing(20)
        layout.addWidget(database)
        layout.addSpacing(20)
        layout.addWidget(provider)

        layout.addStretch()

        layout.addWidget(version, alignment=Qt.AlignRight)