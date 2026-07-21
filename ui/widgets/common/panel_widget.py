from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
)

from PySide6.QtCore import Qt


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

        #
        # PANEL SETTINGS
        #

        self.setObjectName(
            "GuardianPanel"
        )

        #
        # MAIN LAYOUT
        #

        self.main_layout = QVBoxLayout()

        self.main_layout.setSpacing(
            15
        )

        self.main_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        #
        # TITLE
        #

        self.title_label = QLabel(
            self.title
        )

        self.title_label.setObjectName(
            "GuardianPanelTitle"
        )

        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.main_layout.addWidget(
            self.title_label
        )

        #
        # SET LAYOUT
        #

        self.setLayout(
            self.main_layout
        )

    def setup_styles(self):

        self.setStyleSheet(
            """
            QFrame#GuardianPanel {

                background-color: #1B1B1B;
                border: 2px solid #D4AF37;
                border-radius: 12px;

            }

            QLabel#GuardianPanelTitle {

                color: #D4AF37;
                font-size: 16px;
                font-weight: bold;
                padding-bottom: 5px;

            }

            QLabel {

                color: white;
                font-size: 11pt;

            }
            """
        )

    def add_widget(
        self,
        widget: QWidget,
    ):

        self.main_layout.addWidget(
            widget
        )

    def add_layout(
        self,
        layout,
    ):

        self.main_layout.addLayout(
            layout
        )