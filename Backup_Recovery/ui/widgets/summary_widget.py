from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.panels.summary_panel import (
    SummaryPanel,
)


class SummaryWidget(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            SummaryPanel()
        )

        self.setLayout(
            layout
        )