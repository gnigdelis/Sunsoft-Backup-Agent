from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from ui.v2.styles.theme import Theme


class SecondaryButton(QPushButton):

    def __init__(
        self,
        text: str,
        icon: str = "",
        parent=None,
    ):

        super().__init__(parent)

        if icon:
            self.setText(f"{icon}  {text}")
        else:
            self.setText(text)

        self.setCursor(Qt.PointingHandCursor)

        self.setMinimumHeight(46)

        self.setStyleSheet(f"""
            QPushButton {{

                background:{Theme.Colors.SURFACE_LIGHT};
                color:{Theme.Colors.TEXT};

                border:1px solid {Theme.Colors.BORDER};
                border-radius:10px;

                font-size:11pt;
                font-weight:600;

                padding-left:18px;
                padding-right:18px;

            }}

            QPushButton:hover {{

                background:#3A3D45;

            }}

            QPushButton:pressed {{

                background:#31343B;

            }}
        """)