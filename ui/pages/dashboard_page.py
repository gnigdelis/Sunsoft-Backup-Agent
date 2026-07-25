from PySide6.QtCore import (
    QThread,
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from core.backup_worker import (
    BackupWorker,
)

from ui.widgets.header_widget import (
    HeaderWidget,
)

from ui.panels.summary_panel import (
    SummaryPanel,
)

from ui.panels.information_panel import (
    InformationPanel,
)

from ui.panels.operations_panel import (
    OperationsPanel,
)

from ui.widgets.footer_widget import (
    FooterWidget,
)


class DashboardPage(QWidget):

    def __init__(self):

        super().__init__()

        self.thread = None
        self.worker = None

        self.setup_ui()

        self.connect_signals()

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        main_layout.setSpacing(
            15
        )

        main_layout.addWidget(
            HeaderWidget()
        )

        main_layout.addWidget(
            SummaryPanel()
        )

        main_layout.addWidget(
            InformationPanel()
        )

        self.operations_panel = (
            OperationsPanel()
        )

        main_layout.addWidget(
            self.operations_panel
        )

        main_layout.addWidget(
            FooterWidget()
        )

        self.setLayout(
            main_layout
        )

    def connect_signals(self):

        self.operations_panel \
            .action_buttons_widget \
            .backup_requested.connect(

                self.execute_backup

            )

    def execute_backup(self):

        logs = (
            self.operations_panel.logs_widget
        )

        logs.clear_logs()

        logs.add_info_log(
            "Το Backup ξεκίνησε..."
        )

        self.operations_panel \
            .action_buttons_widget \
            .setEnabled(
                False
            )

        #
        # THREAD
        #

        self.thread = QThread()

        self.worker = BackupWorker()

        self.worker.moveToThread(
            self.thread
        )

        #
        # LIVE LOGS
        #

        self.worker.log_info.connect(
            logs.add_info_log
        )

        self.worker.log_success.connect(
            logs.add_success_log
        )

        self.worker.log_error.connect(
            logs.add_error_log
        )

        #
        # THREAD SIGNALS
        #

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.backup_finished
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.start()

    def backup_finished(
        self,
        result,
    ):

        if result["success"]:

            self.operations_panel.logs_widget.add_success_log(
                "Το Backup ολοκληρώθηκε επιτυχώς."
            )

        else:

            errors = result.get(
                "errors",
                [
                    "Άγνωστο σφάλμα."
                ]
            )

            self.operations_panel.logs_widget.add_error_log(
                errors[0]
            )

        self.operations_panel \
            .action_buttons_widget \
            .setEnabled(
                True
            )

        self.worker = None
        self.thread = None