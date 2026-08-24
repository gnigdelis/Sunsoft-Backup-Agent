from pathlib import Path

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QHBoxLayout


class SvgIcon(QWidget):
    """
    Lightweight SVG icon widget used across the entire UI.

    Lucide icons are normalized to white stroke so they remain
    consistent inside the colored icon containers.
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

    def _prepare_svg(self, data: bytes):

        svg = data.decode(
            "utf-8",
            errors="ignore",
        )

        #
        # Lucide normally uses currentColor.
        # QSvgWidget does not inherit CSS currentColor
        # the way a browser does, so force the stroke to white.
        #

        svg = svg.replace(
            'stroke="currentColor"',
            'stroke="#ffffff"',
        )

        svg = svg.replace(
            'stroke="black"',
            'stroke="#ffffff"',
        )

        svg = svg.replace(
            'stroke="#000"',
            'stroke="#ffffff"',
        )

        svg = svg.replace(
            'stroke="#000000"',
            'stroke="#ffffff"',
        )

        return svg.encode("utf-8")

    def load(self, filename: str):

        path = self._resolve_path(filename)

        if path is None:
            return

        try:

            data = path.read_bytes()

            prepared = self._prepare_svg(
                data
            )

            self._icon.load(
                QByteArray(prepared)
            )

        except Exception:
            pass

    def setSize(self, size: int):

        self._size = size

        self._icon.setFixedSize(
            size,
            size,
        )

        self.setFixedSize(
            size,
            size,
        )

    @property
    def size(self):
        return self._size
