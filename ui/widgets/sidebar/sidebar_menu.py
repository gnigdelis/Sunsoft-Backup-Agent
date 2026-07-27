from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from ui.styles.theme import (
    BUTTON_BACKGROUND,
    BUTTON_HOVER_BACKGROUND,
    BUTTON_BORDER_COLOR,
    BUTTON_BORDER_RADIUS,
    BUTTON_HEIGHT,
    TEXT_FONT_SIZE,
    PRIMARY_COLOR,
    WHITE_COLOR,
)


class SidebarMenu(QWidget):

    dashboard_clicked = Signal()
    history_clicked = Signal()
    settings_clicked = Signal()

    def __init__(self):

        super().__init__()

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.dashboard_button = QPushButton("🏠  Dashboard")
        self.history_button = QPushButton("🕘  Ιστορικό Backup")
        self.settings_button = QPushButton("⚙️  Ρυθμίσεις")

        self.buttons = [

            self.dashboard_button,
            self.history_button,
            self.settings_button,

        ]

        for button in self.buttons:

            button.setCursor(Qt.PointingHandCursor)
            button.setMinimumHeight(BUTTON_HEIGHT)

            layout.addWidget(button)

        layout.addStretch()

        self.setLayout(layout)

        self.apply_styles()

        self.set_active_button(
            self.dashboard_button
        )

    def connect_signals(self):

        self.dashboard_button.clicked.connect(

            lambda: self.button_clicked(
                self.dashboard_button,
                self.dashboard_clicked,
            )

        )

        self.history_button.clicked.connect(

            lambda: self.button_clicked(
                self.history_button,
                self.history_clicked,
            )

        )

        self.settings_button.clicked.connect(

            lambda: self.button_clicked(
                self.settings_button,
                self.settings_clicked,
            )

        )

    def button_clicked(self, button, signal):

        self.set_active_button(button)

        signal.emit()

    def set_active_button(self, active_button):

        for button in self.buttons:

            if button == active_button:

                button.setStyleSheet(

                    f"""
                    QPushButton {{

                        background:{PRIMARY_COLOR};
                        color:{WHITE_COLOR};

                        border:none;
                        border-radius:{BUTTON_BORDER_RADIUS}px;

                        padding-left:18px;

                        font-size:{TEXT_FONT_SIZE}pt;
                        font-weight:600;
                        text-align:left;

                    }}
                    """

                )

            else:

                button.setStyleSheet(

                    f"""
                    QPushButton {{

                        background:{BUTTON_BACKGROUND};
                        color:{WHITE_COLOR};

                        border:1px solid {BUTTON_BORDER_COLOR};
                        border-radius:{BUTTON_BORDER_RADIUS}px;

                        padding-left:18px;

                        font-size:{TEXT_FONT_SIZE}pt;
                        text-align:left;

                    }}

                    QPushButton:hover {{

                        background:{BUTTON_HOVER_BACKGROUND};

                    }}
                    """

                )

    def apply_styles(self):

        self.set_active_button(
            self.dashboard_button
        )