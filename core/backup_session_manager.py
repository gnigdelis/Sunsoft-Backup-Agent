from pathlib import Path
from datetime import datetime
import platform

from core.common.result import Result


class BackupSessionManager:

    def _get_computer_name(self):

        return platform.node()

    def _get_timestamp(self):

        return datetime.now().strftime(
            "%d%m%Y_%H%M%S"
        )

    def _get_session_name(self):

        computer_name = (
            self._get_computer_name()
        )

        timestamp = (
            self._get_timestamp()
        )

        return (
            f"{computer_name}_{timestamp}"
        )

    def create_session(
        self,
        destination_path,
    ):

        try:

            session_name = (
                self._get_session_name()
            )

            session_path = (
                Path(destination_path)
                / session_name
            )

            session_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "computer_name":
                        self._get_computer_name(),
                    "session_name":
                        session_name,
                    "session_path":
                        str(session_path),
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )