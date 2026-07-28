from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
)

from ui.v2.styles.theme import Theme


class ProgressCard(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        self.title = QLabel("Backup Progress")
        self.title.setFont(Theme.Typography.heading())
        self.title.setStyleSheet(
            f"color:{Theme.Colors.TEXT};"
        )

        self.percent = QLabel("0%")
        self.percent.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            font-size:11pt;
            """
        )

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(18)

        self.progress.setStyleSheet(f"""
            QProgressBar {{

                border: none;
                border-radius: 9px;
                background: {Theme.Colors.SURFACE_LIGHT};

            }}

            QProgressBar::chunk {{

                border-radius: 9px;
                background: #E53935;

            }}
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.percent)
        layout.addWidget(self.progress)

        self.setStyleSheet(f"""
            ProgressCard {{

                background: {Theme.Colors.SURFACE};
                border: 1px solid {Theme.Colors.BORDER};
                border-radius: 12px;

            }}
        """)

    def set_progress(self, value: int):

        value = max(0, min(100, value))

        self.progress.setValue(value)
        self.percent.setText(f"{value}%")