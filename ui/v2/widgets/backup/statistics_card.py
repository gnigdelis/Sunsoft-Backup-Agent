from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QVBoxLayout,
)

from ui.v2.styles.theme import Theme


class StatisticsCard(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(15)

        title = QLabel("Backup Statistics")

        title.setFont(
             Theme.Typography.heading()
        )

        title.setStyleSheet(
            f"color:{Theme.Colors.TEXT};"
        )

        grid = QGridLayout()
        grid.setHorizontalSpacing(25)
        grid.setVerticalSpacing(12)

        self.files = QLabel("0")
        self.size = QLabel("0 MB")
        self.duration = QLabel("00:00")
        self.compression = QLabel("0 %")

        values = [
            self.files,
            self.size,
            self.duration,
            self.compression,
        ]

        for value in values:
            value.setStyleSheet(f"""
                color:{Theme.Colors.TEXT};
                font-size:11pt;
                font-weight:600;
            """)

        grid.addWidget(QLabel("📄 Files"), 0, 0)
        grid.addWidget(self.files, 0, 1)

        grid.addWidget(QLabel("💾 Size"), 1, 0)
        grid.addWidget(self.size, 1, 1)

        grid.addWidget(QLabel("⏱ Duration"), 2, 0)
        grid.addWidget(self.duration, 2, 1)

        grid.addWidget(QLabel("🗜 Compression"), 3, 0)
        grid.addWidget(self.compression, 3, 1)

        root.addWidget(title)
        root.addLayout(grid)

        self.setStyleSheet(f"""
            StatisticsCard {{

                background:{Theme.Colors.SURFACE};

                border:1px solid {Theme.Colors.BORDER};

                border-radius:12px;

            }}

            QLabel {{

                color:{Theme.Colors.TEXT};

            }}
        """)

    def set_statistics(
        self,
        files: int,
        size: str,
        duration: str,
        compression: str,
    ):

        self.files.setText(str(files))
        self.size.setText(size)
        self.duration.setText(duration)
        self.compression.setText(compression)