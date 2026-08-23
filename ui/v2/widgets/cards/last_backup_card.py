from datetime import datetime
from pathlib import Path
import json
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from ui.v2.widgets.cards.base_card import BaseCard
from ui.v2.widgets.common.status_chip import StatusChip
from ui.v2.styles.theme import Theme


class LastBackupCard(BaseCard):

    STATE_DIRECTORY = (
        Path(
            os.environ.get(
                "LOCALAPPDATA",
                Path.home(),
            )
        )
        / "Sunsoft Backup Agent"
    )

    STATE_FILE = (
        STATE_DIRECTORY
        / "last_backup.json"
    )

    def __init__(self):

        super().__init__(
            title="Last Backup",
        )

        self.build()

        self.load_last_backup()

    # =====================================================
    # UI
    # =====================================================

    def build(self):

        self.time_label = QLabel(
            "Never"
        )

        self.time_label.setFont(
            Theme.Typography.title()
        )

        self.time_label.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT};
            font-size:22pt;
            font-weight:700;
            """
        )

        self.date_label = QLabel(
            "-"
        )

        self.date_label.setFont(
            Theme.Typography.body()
        )

        self.date_label.setStyleSheet(
            f"""
            color:{Theme.Colors.TEXT_SECONDARY};
            """
        )

        self.status_chip = StatusChip(
            "NO BACKUP",
            "warning",
        )

        self.status_chip.setFixedWidth(
            100
        )

        self.status_chip.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.add_widget(
            self.time_label
        )

        self.add_widget(
            self.date_label
        )

        self.add_widget(
            self.status_chip
        )

        self.content_layout.addStretch()

    # =====================================================
    # SAVE LAST BACKUP
    # =====================================================

    def save_last_backup(
        self,
        backup_datetime,
    ):

        try:

            self.STATE_DIRECTORY.mkdir(
                parents=True,
                exist_ok=True,
            )

            data = {
                "last_backup":
                    backup_datetime.isoformat(),
            }

            with open(
                self.STATE_FILE,
                "w",
                encoding="utf-8",
            ) as state_file:

                json.dump(
                    data,
                    state_file,
                    ensure_ascii=False,
                    indent=4,
                )

        except Exception:
            pass

    # =====================================================
    # LOAD LAST BACKUP
    # =====================================================

    def load_last_backup(self):

        try:

            if not self.STATE_FILE.exists():
                return

            with open(
                self.STATE_FILE,
                "r",
                encoding="utf-8",
            ) as state_file:

                data = json.load(
                    state_file
                )

            value = data.get(
                "last_backup"
            )

            if not value:
                return

            backup_datetime = datetime.fromisoformat(
                value
            )

            self.show_backup(
                backup_datetime
            )

        except Exception:
            return

    # =====================================================
    # SHOW BACKUP
    # =====================================================

    def show_backup(
        self,
        backup_datetime,
    ):

        now = datetime.now()

        if backup_datetime.date() == now.date():

            self.time_label.setText(
                backup_datetime.strftime(
                    "Today %H:%M"
                )
            )

        else:

            self.time_label.setText(
                backup_datetime.strftime(
                    "%d/%m/%Y %H:%M"
                )
            )

        self.date_label.setText(
            backup_datetime.strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        )

        self.status_chip.setText(
            "SUCCESS"
        )

        self.status_chip.setStyleSheet(
            f"""
            background:{Theme.Colors.SUCCESS};
            color:white;
            border-radius:10px;
            padding:4px 8px;
            font-weight:600;
            """
        )

    # =====================================================
    # BACKUP COMPLETED
    # =====================================================

    def update_backup(self):

        now = datetime.now()

        self.save_last_backup(
            now
        )

        self.show_backup(
            now
        )

    # =====================================================
    # BACKUP FAILED
    # =====================================================

    def set_failed(self):

        self.status_chip.setText(
            "FAILED"
        )

        self.status_chip.setStyleSheet(
            f"""
            background:{Theme.Colors.ERROR};
            color:white;
            border-radius:10px;
            padding:4px 8px;
            font-weight:600;
            """
        )