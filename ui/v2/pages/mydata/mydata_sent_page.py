from PySide6.QtCore import (
    Qt,
    QDate,
    QSettings,
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QAbstractItemView,
    QApplication,
)

from core.mydata.mydata_service import MyDataService
from core.mydata.mydata_pdf import MyDataPDF


class MyDataSentPage(QWidget):

    def __init__(self):

        super().__init__()

        self.service = MyDataService()

        self.invoices = []

        self.setup_ui()

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        layout.setSpacing(12)

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title = QLabel(
            "MyData Sent"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 24pt;
                font-weight: 700;
            }
            """
        )

        layout.addWidget(title)

        # -------------------------------------------------
        # DATE SEARCH
        # -------------------------------------------------

        search_layout = QHBoxLayout()

        from_label = QLabel(
            "Από:"
        )

        self.from_date = QDateEdit()

        self.from_date.setCalendarPopup(
            True
        )

        self.from_date.setDate(
            QDate.currentDate().addMonths(-1)
        )

        self.from_date.setDisplayFormat(
            "dd/MM/yyyy"
        )

        to_label = QLabel(
            "Έως:"
        )

        self.to_date = QDateEdit()

        self.to_date.setCalendarPopup(
            True
        )

        self.to_date.setDate(
            QDate.currentDate()
        )

        self.to_date.setDisplayFormat(
            "dd/MM/yyyy"
        )

        self.search_button = QPushButton(
            "Έρευνα"
        )

        self.search_button.clicked.connect(
            self.search
        )

        search_layout.addWidget(
            from_label
        )

        search_layout.addWidget(
            self.from_date
        )

        search_layout.addWidget(
            to_label
        )

        search_layout.addWidget(
            self.to_date
        )

        search_layout.addWidget(
            self.search_button
        )

        search_layout.addStretch()

        layout.addLayout(
            search_layout
        )

        # -------------------------------------------------
        # ACTIONS
        # -------------------------------------------------

        actions_layout = QHBoxLayout()

        self.send_selected_button = QPushButton(
            "Αποστολή Επιλεγμένων"
        )

        self.send_selected_button.clicked.connect(
            self.send_selected
        )

        self.send_all_button = QPushButton(
            "Αποστολή Όλων"
        )

        self.send_all_button.clicked.connect(
            self.send_all
        )

        self.delete_button = QPushButton(
            "Διαγραφή MyDATA"
        )

        self.delete_button.clicked.connect(
            self.delete_mydata
        )

        self.pdf_button = QPushButton(
            "Εκτύπωση PDF"
        )

        self.pdf_button.clicked.connect(
            self.print_pdf
        )

        actions_layout.addWidget(
            self.send_selected_button
        )

        actions_layout.addWidget(
            self.send_all_button
        )

        actions_layout.addWidget(
            self.delete_button
        )

        actions_layout.addWidget(
            self.pdf_button
        )

        actions_layout.addStretch()

        layout.addLayout(
            actions_layout
        )

        # -------------------------------------------------
        # COUNT
        # -------------------------------------------------

        self.count_label = QLabel(
            "ΠΛΗΘΟΣ: 0"
        )

        layout.addWidget(
            self.count_label
        )

        # -------------------------------------------------
        # TABLE
        # -------------------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels(
            [
                "Επιλογή",
                "ΤΥΠΟΣ",
                "ΟΝΟΜΑ",
                "ΗΜ/ΝΙΑ",
                "Α/Α",
                "ΑΦΜ",
                "ID",
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # -------------------------------------------------
        # COLUMN RESIZING
        # -------------------------------------------------

        header = self.table.horizontalHeader()

        # Αρχικά υπολογίζουμε λογικά πλάτη
        # σύμφωνα με το περιεχόμενο.
        header.resizeSections(
            QHeaderView.ResizeMode.ResizeToContents
        )

        # Από εδώ και πέρα ο χειριστής μπορεί
        # να αλλάξει ελεύθερα οποιαδήποτε στήλη.
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )

        # Η τελευταία στήλη δεν θα γεμίζει αυτόματα
        # όλο τον διαθέσιμο χώρο.
        header.setStretchLastSection(
            False
        )

        # Αποθήκευση κάθε αλλαγής πλάτους.
        header.sectionResized.connect(
            self.save_column_widths
        )

        # Επαναφορά των πλατών που είχε επιλέξει
        # ο χειριστής σε προηγούμενη εκκίνηση.
        self.load_column_widths()

        self.table.setAlternatingRowColors(
            True
        )

        layout.addWidget(
            self.table,
            1,
        )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        self.status_label = QLabel(
            "Έτοιμο."
        )

        layout.addWidget(
            self.status_label
        )

    # =====================================================
    # COLUMN WIDTHS
    # =====================================================

    def save_column_widths(
        self,
        *args,
    ):

        try:

            settings = QSettings(
                "Sunsoft",
                "SupportAgent",
            )

            widths = []

            for column in range(
                self.table.columnCount()
            ):

                widths.append(
                    self.table.columnWidth(
                        column
                    )
                )

            settings.setValue(
                "MyDataSent/ColumnWidths",
                widths,
            )

            settings.sync()

        except Exception:

            pass

    def load_column_widths(self):

        try:

            settings = QSettings(
                "Sunsoft",
                "SupportAgent",
            )

            widths = settings.value(
                "MyDataSent/ColumnWidths"
            )

            if not widths:

                return

            for column, width in enumerate(
                widths
            ):

                if column >= self.table.columnCount():

                    break

                try:

                    width = int(
                        width
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    continue

                if width < 30:

                    width = 30

                self.table.setColumnWidth(
                    column,
                    width,
                )

        except Exception:

            pass

    # =====================================================
    # SEARCH
    # =====================================================

    def search(self):

        start = self.from_date.date().toString(
            "yyyyMMdd"
        )

        end = self.to_date.date().toString(
            "yyyyMMdd"
        )

        if start > end:

            QMessageBox.warning(
                self,
                "MyData Sent",
                "Η ημερομηνία Από δεν μπορεί "
                "να είναι μεγαλύτερη από την ημερομηνία Έως.",
            )

            return

        if not self.service.database_selected():

            QMessageBox.warning(
                self,
                "MyData Sent",
                "Δεν έχει επιλεγεί βάση δεδομένων.",
            )

            return

        self.status_label.setText(
            "Αναζήτηση παραστατικών..."
        )

        QApplication.processEvents()

        try:

            self.invoices = self.service.search(
                start,
                end,
            )

            self.populate_table()

            self.status_label.setText(
                "Η αναζήτηση ολοκληρώθηκε."
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Σφάλμα",
                str(exc),
            )

            self.status_label.setText(
                "Η αναζήτηση απέτυχε."
            )

    # =====================================================
    # TABLE
    # =====================================================

    def populate_table(self):

        self.table.setRowCount(0)

        for row_index, invoice in enumerate(
            self.invoices
        ):

            self.table.insertRow(
                row_index
            )

            checkbox = QTableWidgetItem()

            checkbox.setFlags(
                checkbox.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )

            checkbox.setCheckState(
                Qt.CheckState.Unchecked
            )

            self.table.setItem(
                row_index,
                0,
                checkbox,
            )

            values = [
                invoice.invoice_type,
                invoice.document_name,
                invoice.issue_date,
                invoice.aa,
                invoice.cust_afm,
                str(invoice.invoice_id),
            ]

            for column, value in enumerate(
                values,
                start=1,
            ):

                item = QTableWidgetItem(
                    value
                )

                self.table.setItem(
                    row_index,
                    column,
                    item,
                )

        self.count_label.setText(
            f"ΠΛΗΘΟΣ: {len(self.invoices)}"
        )

    # =====================================================
    # SELECTED
    # =====================================================

    def get_selected_invoices(self):

        selected = []

        for row in range(
            self.table.rowCount()
        ):

            item = self.table.item(
                row,
                0,
            )

            if (
                item
                and
                item.checkState()
                == Qt.CheckState.Checked
            ):

                if row < len(
                    self.invoices
                ):

                    selected.append(
                        self.invoices[row]
                    )

        return selected

    # =====================================================
    # SEND SELECTED
    # =====================================================

    def send_selected(self):

        invoices = (
            self.get_selected_invoices()
        )

        if not invoices:

            QMessageBox.information(
                self,
                "MyData Sent",
                "Δεν έχουν επιλεγεί παραστατικά.",
            )

            return

        self.send_invoices(
            invoices
        )

    # =====================================================
    # SEND ALL
    # =====================================================

    def send_all(self):

        if not self.invoices:

            QMessageBox.information(
                self,
                "MyData Sent",
                "Δεν υπάρχουν παραστατικά.",
            )

            return

        answer = QMessageBox.question(
            self,
            "Αποστολή Όλων",
            (
                f"Θέλεις να αποσταλούν "
                f"όλα τα {len(self.invoices)} "
                "παραστατικά;"
            ),
        )

        if answer != QMessageBox.StandardButton.Yes:

            return

        self.send_invoices(
            self.invoices
        )

    # =====================================================
    # SEND
    # =====================================================

    def send_invoices(
        self,
        invoices,
    ):

        self.status_label.setText(
            "Αποστολή παραστατικών..."
        )

        QApplication.setOverrideCursor(
            Qt.CursorShape.WaitCursor
        )

        try:

            results = (
                self.service.send_invoices(
                    invoices
                )
            )

            success_count = sum(
                1
                for item in results
                if item["result"]["success"]
            )

            failed_count = (
                len(results)
                - success_count
            )

            self.status_label.setText(
                (
                    f"Ολοκληρώθηκε: "
                    f"{success_count} επιτυχίες, "
                    f"{failed_count} αποτυχίες."
                )
            )

            self.update_table_after_send()

            if failed_count:

                QMessageBox.warning(
                    self,
                    "MyData Sent",
                    (
                        "Η αποστολή ολοκληρώθηκε.\n\n"
                        f"Επιτυχίες: {success_count}\n"
                        f"Αποτυχίες: {failed_count}"
                    ),
                )

            else:

                QMessageBox.information(
                    self,
                    "MyData Sent",
                    (
                        "Η αποστολή ολοκληρώθηκε "
                        f"επιτυχώς για {success_count} "
                        "παραστατικά."
                    ),
                )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Σφάλμα Αποστολής",
                str(exc),
            )

        finally:

            QApplication.restoreOverrideCursor()

    # =====================================================
    # UPDATE TABLE
    # =====================================================

    def update_table_after_send(self):

        for row, invoice in enumerate(
            self.invoices
        ):

            if invoice.sent:

                item = self.table.item(
                    row,
                    0,
                )

                if item:

                    item.setCheckState(
                        Qt.CheckState.Unchecked
                    )

                for column in range(
                    self.table.columnCount()
                ):

                    cell = self.table.item(
                        row,
                        column,
                    )

                    if cell:

                        cell.setToolTip(
                            "Απεστάλη επιτυχώς."
                        )

    # =====================================================
    # DELETE MYDATA
    # =====================================================

    def delete_mydata(self):

        QMessageBox.information(
            self,
            "Διαγραφή MyDATA",
            (
                "Η λειτουργία διαγραφής MyDATA "
                "θα συνδεθεί αφού επιβεβαιώσουμε "
                "την ακριβή λειτουργία του MUPT."
            ),
        )

    # =====================================================
    # PDF
    # =====================================================

    def print_pdf(self):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.information(
                self,
                "PDF",
                "Επίλεξε πρώτα ένα παραστατικό.",
            )

            return

        if row >= len(
            self.invoices
        ):

            return

        invoice = self.invoices[row]

        if not invoice.sent:

            QMessageBox.warning(
                self,
                "PDF",
                (
                    "Το παραστατικό πρέπει "
                    "να έχει αποσταλεί επιτυχώς "
                    "πριν την εκτύπωση PDF."
                ),
            )

            return

        try:

            success = MyDataPDF.save_invoice(
                invoice,
                self,
            )

            if success:

                self.status_label.setText(
                    "Το PDF αποθηκεύτηκε επιτυχώς."
                )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "PDF",
                str(exc),
            )