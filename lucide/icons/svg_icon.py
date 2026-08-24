from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QHBoxLayout


class SvgIcon(QWidget):
    """
    Lightweight SVG icon widget used across the entire UI.

    Supported sources:
        SvgIcon("navigation/dashboard.svg")
        SvgIcon("system/storage.svg")
        SvgIcon("lucide/icons/house.svg")

    The loader first checks assets/icons and then the path itself.
    """

    def __init__(
        self,
        filename: str,
        size: int = 24,
        parent=None,
    ):
        super().__init__(parent)

        self._size = size

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._icon = QSvgWidget(self)
        self._icon.setFixedSize(size, size)

        layout.addWidget(self._icon)

        self.setFixedSize(size, size)

        self.load(filename)

    def _resolve_path(self, filename: str):

        candidates = [
            Path("assets") / "icons" / filename,
            Path(filename),
        ]

        for candidate in candidates:

            if candidate.exists():
                return candidate

        return None

    def load(self, filename: str):

        path = self._resolve_path(filename)

        if path is not None:
            self._icon.load(str(path))

    def setSize(self, size: int):

        self._size = size

        self._icon.setFixedSize(size, size)
        self.setFixedSize(size, size)

    @property
    def size(self):
        return self._size
