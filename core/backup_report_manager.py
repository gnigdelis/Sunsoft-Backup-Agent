from pathlib import Path
from datetime import datetime
import platform

from core.common.result import Result


class BackupReportManager:

    def create_report(
        self,
        session_path,
        report_lines,
    ):

        try:

            report_file = (
                Path(session_path)
                / "Backup_Report.txt"
            )

            with open(
                report_file,
                "w",
                encoding="utf-8",
            ) as report:

                report.write("=" * 60 + "\n")
                report.write("SUNSOFT SUPPORT AGENT\n")
                report.write("=" * 60 + "\n\n")

                report.write(
                    f"Computer Name : {platform.node()}\n"
                )

                report.write(
                    f"Backup Date : {datetime.now().strftime('%d/%m/%Y')}\n"
                )

                report.write(
                    f"Backup Time : {datetime.now().strftime('%H:%M:%S')}\n"
                )

                report.write(
                    f"Windows Version : {platform.platform()}\n\n"
                )

                report.write(
                    "BACKUP RESULTS\n"
                )

                report.write(
                    "-" * 60 + "\n"
                )

                for line in report_lines:

                    report.write(
                        line + "\n"
                    )

                report.write("\n")
                report.write("=" * 60 + "\n")
                report.write(
                    "Backup Completed.\n"
                )
                report.write("=" * 60 + "\n")

            return Result.success(

                data={

                    "status": "SUCCESS",

                    "report_file":
                        str(report_file),

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )