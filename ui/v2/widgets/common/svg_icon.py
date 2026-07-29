from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QHBoxLayout


class SvgIcon(QWidget):
    def __init__(
        self,
        filename: str,
        size: int = 24,
        parent=None,
    ):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon = QSvgWidget()

        icon_path = Path("assets") / "icons" / filename

        self.icon.load(str(icon_path))
        self.icon.setFixedSize(size, size)

        layout.addWidget(self.icon)

        self.setFixedSize(size, size)