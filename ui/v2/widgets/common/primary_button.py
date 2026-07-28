from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton

from ui.v2.styles.theme import Theme


class PrimaryButton(QPushButton):

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

                background:#e53935;
                color:white;

                border:none;
                border-radius:10px;

                font-size:11pt;
                font-weight:600;

                padding-left:18px;
                padding-right:18px;

            }}

            QPushButton:hover {{

                background:#ef5350;

            }}

            QPushButton:pressed {{

                background:#c62828;

            }}

            QPushButton:disabled {{

                background:{Theme.Colors.SURFACE_LIGHT};
                color:#888;

            }}
        """)