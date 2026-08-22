from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
)

from ui.styles.theme import (
    PANEL_BACKGROUND,
    PANEL_BORDER_COLOR,
    PANEL_BORDER_RADIUS,
    PRIMARY_COLOR,
    WHITE_COLOR,
)


class PanelWidget(QFrame):

    def __init__(
        self,
        title: str,
    ):

        super().__init__()

        self.title = title

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):

        self.setObjectName("PanelWidget")

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        #
        # MAIN LAYOUT
        #

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )

        self.main_layout.setSpacing(10)

        #
        # TITLE
        #

        self.title_label = QLabel(self.title)

        self.title_label.setObjectName("PanelTitle")

        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignVCenter
        )

        self.main_layout.addWidget(self.title_label)

        #
        # SPACE AFTER TITLE
        #

        self.main_layout.addSpacing(6)

    def setup_styles(self):

        self.setStyleSheet(
            f"""
            QFrame#PanelWidget {{
                background-color: {PANEL_BACKGROUND};
                border: 1px solid {PANEL_BORDER_COLOR};
                border-radius: {PANEL_BORDER_RADIUS}px;
            }}

            QLabel#PanelTitle {{
                color: {PRIMARY_COLOR};
                font-size: 13pt;
                font-weight: 700;
                border: none;
            }}

            QLabel {{
                color: {WHITE_COLOR};
                border: none;
            }}
            """
        )

    def add_widget(
        self,
        widget: QWidget,
    ):

        self.main_layout.addWidget(widget)

    def add_layout(
        self,
        layout,
    ):

        self.main_layout.addLayout(layout)