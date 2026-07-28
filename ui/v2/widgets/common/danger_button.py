from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class DangerButton(QPushButton):

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

        self.setStyleSheet("""
            QPushButton {

                background:#C62828;
                color:white;

                border:none;
                border-radius:10px;

                font-size:11pt;
                font-weight:600;

                padding-left:18px;
                padding-right:18px;

            }

            QPushButton:hover {

                background:#D32F2F;

            }

            QPushButton:pressed {

                background:#B71C1C;

            }
        """)