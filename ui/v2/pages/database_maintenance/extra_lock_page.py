from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QPushButton,
    QFrame,
    QMessageBox,
    QScrollArea,
)

from core.database.database_context import database_context
from core.maintenance.extra_lock_service import (
    extra_lock_service,
)


class ExtraLockPage(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.spinboxes = []

        self.setup_ui()

        database_context.database_changed.connect(
            self.on_database_changed
        )

        self.load_values()

    def setup_ui(self):

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )

        main_layout.setSpacing(
            12
        )

        #
        # Main card
        #

        card = QFrame()

        card.setObjectName(
            "ExtraLockCard"
        )

        card_layout = QVBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        card_layout.setSpacing(
            12
        )

        #
        # Title
        #

        title = QLabel(
            "Extra Lock"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            """
        )

        card_layout.addWidget(
            title
        )

        #
        # Description
        #

        description = QLabel(
            "Προβολή και διαχείριση των ενεργών "
            "Extra Lock επιλογών της βάσης."
        )

        description.setWordWrap(
            True
        )

        description.setStyleSheet(
            """
            QLabel {
                color: #bdbdbd;
                font-size: 13px;
            }
            """
        )

        card_layout.addWidget(
            description
        )

        #
        # Database information
        #

        self.database_label = QLabel(
            "Βάση: -"
        )

        self.database_label.setStyleSheet(
            """
            QLabel {
                font-weight: bold;
            }
            """
        )

        card_layout.addWidget(
            self.database_label
        )

        #
        # Scroll area
        #

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.NoFrame
        )

        content = QWidget()

        self.items_layout = QVBoxLayout(
            content
        )

        self.items_layout.setContentsMargins(
            0,
            5,
            0,
            5,
        )

        self.items_layout.setSpacing(
            8
        )

        scroll.setWidget(
            content
        )

        card_layout.addWidget(
            scroll,
            1,
        )

        #
        # Buttons
        #

        buttons_layout = QHBoxLayout()

        buttons_layout.setSpacing(
            10
        )

        self.reload_button = QPushButton(
            "Ανανέωση"
        )

        self.save_button = QPushButton(
            "Αποθήκευση"
        )

        self.reload_button.setMinimumHeight(
            42
        )

        self.save_button.setMinimumHeight(
            42
        )

        self.reload_button.clicked.connect(
            self.load_values
        )

        self.save_button.clicked.connect(
            self.save_values
        )

        buttons_layout.addWidget(
            self.reload_button
        )

        buttons_layout.addStretch()

        buttons_layout.addWidget(
            self.save_button
        )

        card_layout.addLayout(
            buttons_layout
        )

        main_layout.addWidget(
            card
        )

    # ==========================================================
    # Database
    # ==========================================================

    def on_database_changed(
        self,
        database,
    ):

        if not database:

            self.database_label.setText(
                "Βάση: -"
            )

            self.clear_items()

            return

        self.database_label.setText(
            "Βάση: "
            + database.get(
                "name",
                "Unknown",
            )
        )

        self.load_values()

    # ==========================================================
    # Helpers
    # ==========================================================

    def clear_items(self):

        self.spinboxes.clear()

        while self.items_layout.count():

            item = self.items_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

    # ==========================================================
    # Load
    # ==========================================================

    def load_values(self):

        self.clear_items()

        database = (
            database_context.active()
        )

        if not database:

            self.database_label.setText(
                "Βάση: Δεν έχει επιλεγεί"
            )

            self.set_controls_enabled(
                False
            )

            return

        self.database_label.setText(
            "Βάση: "
            + database.get(
                "name",
                "Unknown",
            )
        )

        try:

            result = (
                extra_lock_service.load()
            )

            for item in result["items"]:

                row = QFrame()

                row.setFrameShape(
                    QFrame.StyledPanel
                )

                row_layout = QHBoxLayout(
                    row
                )

                row_layout.setContentsMargins(
                    10,
                    6,
                    10,
                    6,
                )

                name_label = QLabel(
                    item.name
                )

                name_label.setMinimumWidth(
                    180
                )

                value = QSpinBox()

                value.setMinimum(
                    0
                )

                value.setMaximum(
                    999
                )

                value.setValue(
                    item.value
                )

                value.setAlignment(
                    Qt.AlignCenter
                )

                value.setMinimumWidth(
                    90
                )

                row_layout.addWidget(
                    name_label
                )

                row_layout.addStretch()

                row_layout.addWidget(
                    value
                )

                self.items_layout.addWidget(
                    row
                )

                self.spinboxes.append(
                    value
                )

            self.items_layout.addStretch()

            self.set_controls_enabled(
                True
            )

        except Exception as exc:

            self.set_controls_enabled(
                False
            )

            QMessageBox.critical(
                self,
                "Extra Lock",
                f"Αδυναμία ανάγνωσης:\n\n{exc}",
            )

    # ==========================================================
    # Save
    # ==========================================================

    def save_values(self):

        if not database_context.is_selected():

            QMessageBox.warning(
                self,
                "Extra Lock",
                "Δεν έχει επιλεγεί βάση δεδομένων.",
            )

            return

        values = [
            spinbox.value()
            for spinbox in self.spinboxes
        ]

        confirmation = QMessageBox.question(
            self,
            "Επιβεβαίωση",
            "Θέλεις να αποθηκεύσεις τις αλλαγές "
            "στις Extra Lock επιλογές;",
            QMessageBox.Yes
            | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation != QMessageBox.Yes:

            return

        self.set_controls_enabled(
            False
        )

        try:

            result = (
                extra_lock_service.save(
                    values
                )
            )

            QMessageBox.information(
                self,
                "Extra Lock",
                "Οι αλλαγές αποθηκεύτηκαν επιτυχώς.",
            )

            self.load_values()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Extra Lock",
                f"Η αποθήκευση απέτυχε:\n\n{exc}",
            )

            self.set_controls_enabled(
                True
            )

    # ==========================================================
    # Controls
    # ==========================================================

    def set_controls_enabled(
        self,
        enabled,
    ):

        self.reload_button.setEnabled(
            enabled
        )

        self.save_button.setEnabled(
            enabled
        )

        for spinbox in self.spinboxes:

            spinbox.setEnabled(
                enabled
            )