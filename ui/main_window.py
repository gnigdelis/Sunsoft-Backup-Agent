from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sunsoft Guardian")
        self.setFixedSize(900, 700)

        self.setup_ui()

    def create_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def setup_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        #
        # TITLE
        #

        title = QLabel("SUNSOFT GUARDIAN")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        main_layout.addWidget(title)
        main_layout.addWidget(self.create_separator())

        #
        # CUSTOMER NAME
        #

        customer_name = QLabel("Customer Name : Not Configured")
        customer_name.setStyleSheet("font-size: 14px;")

        main_layout.addWidget(customer_name)
        main_layout.addWidget(self.create_separator())

        #
        # STATUS
        #

        status = QLabel("Status : ACTIVE")
        status.setStyleSheet("font-size: 14px;")

        main_layout.addWidget(status)
        main_layout.addWidget(self.create_separator())

        #
        # BACKUP INFORMATION
        #

        last_backup = QLabel("Last Backup : Never")
        next_backup = QLabel("Next Backup : Never")

        last_backup.setStyleSheet("font-size: 14px;")
        next_backup.setStyleSheet("font-size: 14px;")

        main_layout.addWidget(last_backup)
        main_layout.addWidget(next_backup)
        main_layout.addWidget(self.create_separator())

        #
        # BACKUP STATUS
        #

        backup_status = [
            "Files ....................... PENDING",
            "Registry .................... PENDING",
            "SQL Backup .................. PENDING",
            "Compression ................. PENDING",
            "Remote Storage .............. PENDING"
        ]

        for item in backup_status:
            label = QLabel(item)
            label.setStyleSheet("font-size: 14px;")
            main_layout.addWidget(label)

        main_layout.addWidget(self.create_separator())

        #
        # BACKUP SIZE
        #

        backup_size = QLabel("Backup Size : 0 MB")
        backup_size.setStyleSheet("font-size: 14px;")

        main_layout.addWidget(backup_size)
        main_layout.addWidget(self.create_separator())

        #
        # LOGS
        #

        logs_title = QLabel("Logs :")
        logs_title.setStyleSheet("font-size: 14px;")

        logs_box = QTextEdit()
        logs_box.setReadOnly(True)
        logs_box.setText("Waiting for backup...")

        main_layout.addWidget(logs_title)
        main_layout.addWidget(logs_box)
        main_layout.addWidget(self.create_separator())

        #
        # BACKUP BUTTON
        #

        backup_button = QPushButton("BACKUP NOW")
        backup_button.setFixedHeight(50)

        backup_button.setStyleSheet("""

            font-size:18px;
            font-weight:bold;

        """)

        main_layout.addWidget(backup_button)

        self.setLayout(main_layout)