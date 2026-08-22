from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

from core.controllers.backup_controller import BackupController
from core.services.maintenance_service import maintenance_service
from core.database.database_context import database_context

from ui.v2.widgets.logs.live_activity_card import LiveActivityCard
from ui.v2.widgets.actions.quick_actions_card import QuickActionsCard


class OperationsSection(QWidget):

    def __init__(self):

        super().__init__()

        self.controller = BackupController()

        self.setup_ui()

        self.connect_signals()

    def setup_ui(self):

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(15)

        self.live_activity = LiveActivityCard()

        self.quick_actions = QuickActionsCard()

        layout.addWidget(
            self.live_activity,
            3,
        )

        layout.addWidget(
            self.quick_actions,
            1,
        )

        self.setLayout(layout)

    def connect_signals(self):

        #
        # Backup
        #

        self.quick_actions.backup_clicked.connect(
            self.start_backup
        )

        #
        # Delete MyDATA Response
        #

        self.quick_actions.delete_mydata_clicked.connect(
            self.start_database_maintenance
        )

        #
        # Backup Logs
        #

        self.controller.log_info.connect(
            self.on_info
        )

        self.controller.log_success.connect(
            self.on_success
        )

        self.controller.log_error.connect(
            self.on_error
        )

        self.controller.finished.connect(
            self.on_finished
        )

    def start_backup(self):

        self.live_activity.clear_logs()

        self.live_activity.add_log(
            "Backup Started..."
        )

        self.controller.start_backup()

    def start_database_maintenance(self):

        self.live_activity.clear_logs()

        #
        # DATABASE CHECK
        #

        if not database_context.is_selected():

            self.live_activity.add_log(
                "✖ No database selected."
            )

            self.live_activity.add_log(
                "Please select a database from the Dashboard."
            )

            return

        #
        # ACTIVE DATABASE
        #

        database = database_context.active()

        database_name = (
            database.get("name")
            if database
            else "Unknown"
        )

        self.live_activity.add_log(
            f"Delete MyDATA Response Started - {database_name}"
        )

        #
        # MAINTENANCE
        #

        try:

            results = maintenance_service.run()

            for result in results:

                if result["success"]:

                    self.live_activity.add_log(
                        f"✓ {result['step']}"
                    )

                    if result["affected_rows"]:

                        self.live_activity.add_log(
                            f"Affected Rows: "
                            f"{result['affected_rows']}"
                        )

                else:

                    self.live_activity.add_log(
                        f"✖ {result['step']}"
                    )

                    self.live_activity.add_log(
                        result["message"]
                    )

                    return

            self.live_activity.add_log(
                "✓ Database Maintenance Completed"
            )

        except Exception as ex:

            self.live_activity.add_log(
                f"✖ {ex}"
            )

    def on_info(self, text):

        self.live_activity.add_log(
            f"ℹ {text}"
        )

    def on_success(self, text):

        self.live_activity.add_log(
            f"✓ {text}"
        )

    def on_error(self, text):

        self.live_activity.add_log(
            f"✖ {text}"
        )

    def on_finished(self, result):

        if result.get("success", False):

            self.live_activity.add_log(
                "✓ Backup Completed."
            )

        else:

            self.live_activity.add_log(
                "✖ Backup Failed."
            )