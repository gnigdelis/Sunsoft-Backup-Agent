from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QSizePolicy,
)

from PySide6.QtCore import (
    Signal,
)

from ui.widgets.common.panel_widget import (
    PanelWidget,
)

from ui.styles.theme import (
    BUTTON_BACKGROUND,
    BUTTON_HOVER_BACKGROUND,
    BUTTON_BORDER_COLOR,
    BUTTON_BORDER_RADIUS,
    WHITE_COLOR,
    TEXT_FONT_SIZE,
    PRIMARY_COLOR,
    PRIMARY_HOVER_COLOR,
)


class ActionButtonsWidget(QWidget):

    backup_requested = Signal()

    def __init__(self):

        super().__init__()

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):

        #
        # MAIN LAYOUT
        #

        main_layout = QVBoxLayout()

        #
        # PANEL
        #

        panel = PanelWidget(
            "Ενέργειες Backup"
        )

        #
        # SPACING
        #

        panel.main_layout.setSpacing(
            15
        )

        #
        # BUTTONS
        #

        self.start_backup_button = QPushButton(
            "ΔΗΜΙΟΥΡΓΙΑ BACKUP"
        )

        self.validate_button = QPushButton(
            "ΕΛΕΓΧΟΣ ΡΥΘΜΙΣΕΩΝ"
        )

        self.open_backup_folder_button = QPushButton(
            "ΑΝΟΙΓΜΑ BACKUP"
        )

        #
        # HEIGHTS
        #

        self.start_backup_button.setMinimumHeight(
            65
        )

        self.validate_button.setMinimumHeight(
            55
        )

        self.open_backup_folder_button.setMinimumHeight(
            55
        )

        #
        # SIZE POLICY
        #

        self.start_backup_button.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        self.validate_button.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        self.open_backup_folder_button.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        #
        # PRIMARY STYLE
        #

        primary_button_style = f"""

        QPushButton {{

            background-color: {PRIMARY_COLOR};
            color: {WHITE_COLOR};

            border: none;
            border-radius: {BUTTON_BORDER_RADIUS}px;

            font-size: 13pt;
            font-weight: bold;

        }}

        QPushButton:hover {{

            background-color: {PRIMARY_HOVER_COLOR};

        }}

        """

        #
        # SECONDARY STYLE
        #

        secondary_button_style = f"""

        QPushButton {{

            background-color: {BUTTON_BACKGROUND};
            color: {WHITE_COLOR};

            border: 1px solid {BUTTON_BORDER_COLOR};
            border-radius: {BUTTON_BORDER_RADIUS}px;

            font-size: {TEXT_FONT_SIZE}pt;
            font-weight: bold;

        }}

        QPushButton:hover {{

            background-color: {BUTTON_HOVER_BACKGROUND};

        }}

        """

        #
        # APPLY STYLES
        #

        self.start_backup_button.setStyleSheet(
            primary_button_style
        )

        self.validate_button.setStyleSheet(
            secondary_button_style
        )

        self.open_backup_folder_button.setStyleSheet(
            secondary_button_style
        )

        #
        # ADD BUTTONS
        #

        panel.add_widget(
            self.start_backup_button
        )

        panel.add_widget(
            self.validate_button
        )

        panel.add_widget(
            self.open_backup_folder_button
        )

        #
        # ADD PANEL
        #

        main_layout.addWidget(
            panel
        )

        self.setLayout(
            main_layout
        )

    def connect_signals(self):

        self.start_backup_button.clicked.connect(
            self.backup_requested.emit
        )