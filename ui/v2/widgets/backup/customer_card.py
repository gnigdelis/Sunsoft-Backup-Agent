from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFormLayout,
    QVBoxLayout,
)

from ui.v2.styles.theme import Theme


class CustomerCard(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(18, 18, 18, 18)

        root.setSpacing(15)

        title = QLabel("Customer Information")

        title.setFont(
            Theme.Typography.heading()
        )

        title.setStyleSheet(
            f"color:{Theme.Colors.TEXT};"
        )

        form = QFormLayout()

        form.setVerticalSpacing(12)

        form.setHorizontalSpacing(20)

        self.customer = QLabel("-")
        self.sql_server = QLabel("-")
        self.destination = QLabel("-")
        self.cloud = QLabel("-")
        self.last_backup = QLabel("-")

        labels = [
            self.customer,
            self.sql_server,
            self.destination,
            self.cloud,
            self.last_backup,
        ]

        for label in labels:

            label.setStyleSheet(
                f"color:{Theme.Colors.TEXT};"
            )

        form.addRow("🏪 Customer", self.customer)
        form.addRow("🗄 SQL Server", self.sql_server)
        form.addRow("📁 Destination", self.destination)
        form.addRow("☁ Cloud", self.cloud)
        form.addRow("🕒 Last Backup", self.last_backup)

        root.addWidget(title)
        root.addLayout(form)

        self.setStyleSheet(f"""
            CustomerCard {{

                background:{Theme.Colors.SURFACE};

                border:1px solid {Theme.Colors.BORDER};

                border-radius:12px;

            }}

            QLabel {{

                color:{Theme.Colors.TEXT};

            }}
        """)

    def set_customer(
        self,
        customer: str,
        sql_server: str,
        destination: str,
        cloud: str,
        last_backup: str,
    ):

        self.customer.setText(customer)
        self.sql_server.setText(sql_server)
        self.destination.setText(destination)
        self.cloud.setText(cloud)
        self.last_backup.setText(last_backup)
