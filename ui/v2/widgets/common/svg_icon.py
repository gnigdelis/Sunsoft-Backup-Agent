from pathlib import Path

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QHBoxLayout


class SvgIcon(QWidget):
    """
    Lightweight SVG icon widget used across the entire UI.

    Supports dynamic icon colors so navigation items can use
    white in the normal state and the brand red on hover/active.
    """

    def __init__(
        self,
        filename: str,
        size: int = 24,
        color: str = "#ffffff",
        parent=None,
    ):
        super().__init__(parent)

        self._size = size
        self._color = color
        self._filename = filename
        self._raw_data = None

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self._icon = QSvgWidget(
            self
        )

        self._icon.setFixedSize(
            size,
            size,
        )

        layout.addWidget(
            self._icon
        )

        self.setFixedSize(
            size,
            size,
        )

        self.load(
            filename
        )

    # ==========================================================
    # PATH
    # ==========================================================

    def _resolve_path(
        self,
        filename: str,
    ):

        candidates = [
            Path("assets") / "icons" / filename,
            Path(filename),
        ]

        for candidate in candidates:

            if candidate.exists():

                return candidate

        return None

    # ==========================================================
    # SVG PREPARATION
    # ==========================================================

    def _prepare_svg(
        self,
        data: bytes,
    ):

        svg = data.decode(
            "utf-8",
            errors="ignore",
        )

        color = self._color

        #
        # Stroke colors
        #

        replacements = {
            'stroke="currentColor"':
                f'stroke="{color}"',

            'stroke="black"':
                f'stroke="{color}"',

            'stroke="#000"':
                f'stroke="{color}"',

            'stroke="#000000"':
                f'stroke="{color}"',

            'stroke="#ffffff"':
                f'stroke="{color}"',

            'stroke="#FFFFFF"':
                f'stroke="{color}"',
        }

        for old, new in replacements.items():

            svg = svg.replace(
                old,
                new,
            )

        #
        # Fill colors
        #

        fill_replacements = {
            'fill="currentColor"':
                f'fill="{color}"',

            'fill="black"':
                f'fill="{color}"',

            'fill="#000"':
                f'fill="{color}"',

            'fill="#000000"':
                f'fill="{color}"',

            'fill="#ffffff"':
                f'fill="{color}"',

            'fill="#FFFFFF"':
                f'fill="{color}"',
        }

        for old, new in fill_replacements.items():

            svg = svg.replace(
                old,
                new,
            )

        return svg.encode(
            "utf-8"
        )

    # ==========================================================
    # LOAD
    # ==========================================================

    def load(
        self,
        filename: str,
    ):

        path = self._resolve_path(
            filename
        )

        if path is None:

            return

        try:

            self._filename = filename

            self._raw_data = (
                path.read_bytes()
            )

            self._render()

        except Exception:

            pass

    # ==========================================================
    # RENDER
    # ==========================================================

    def _render(self):

        if not self._raw_data:

            return

        try:

            prepared = (
                self._prepare_svg(
                    self._raw_data
                )
            )

            self._icon.load(
                QByteArray(
                    prepared
                )
            )

        except Exception:

            pass

    # ==========================================================
    # COLOR
    # ==========================================================

    def setColor(
        self,
        color: str,
    ):

        self._color = color

        self._render()

    # ==========================================================
    # SIZE
    # ==========================================================

    def setSize(
        self,
        size: int,
    ):

        self._size = size

        self._icon.setFixedSize(
            size,
            size,
        )

        self.setFixedSize(
            size,
            size,
        )

    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def size(self):

        return self._size

    @property
    def color(self):

        return self._color