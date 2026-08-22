from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
)

from ui.styles.theme import (
    WHITE_COLOR,
    SECONDARY_TEXT_COLOR,
)


class InfoRowWidget(QWidget):

    ROW_HEIGHT = 32

    def __init__(
        self,
        title: str,
        value: str,
    ):

        super().__init__()

        self.title = title
        self.value = value

        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):

        self.setMinimumHeight(self.ROW_HEIGHT)
        self.setMaximumHeight(self.ROW_HEIGHT)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            0,
            2,
            0,
            2,
        )

        layout.setSpacing(12)

        #
        # TITLE
        #

        self.title_label = QLabel(self.title)

        self.title_label.setMinimumWidth(150)
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignVCenter
        )

        self.title_label.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Preferred
        )

        #
        # VALUE
        #

        self.value_label = QLabel(self.value)

        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight |
            Qt.AlignmentFlag.AlignVCenter
        )

        self.value_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.value_label.setWordWrap(False)

        self.value_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        self.value_label.setToolTip(self.value)

        #
        # ADD
        #

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def setup_styles(self):

        self.title_label.setStyleSheet(

            f"""
            color: {WHITE_COLOR};
            font-size: 10pt;
            font-weight: 600;
            """
        )

        self.value_label.setStyleSheet(

            f"""
            color: {SECONDARY_TEXT_COLOR};
            font-size: 10pt;
            """
        )

    def set_value(
        self,
        value: str,
    ):

        self.value = value

        self.value_label.setText(value)
        self.value_label.setToolTip(value)