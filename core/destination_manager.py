from pathlib import Path
import os
import shutil
import uuid

from core.common.result import Result
from core.settings_manager import SettingsManager


class DestinationManager:

    TEST_FILE_NAME = (
        ".sunsoft_backup_destination_test"
    )

    def __init__(self):

        self.settings_manager = (
            SettingsManager()
        )

    # ---------------------------------------------------------
    # Destination
    # ---------------------------------------------------------

    def get_destination(self):

        result = (
            self.settings_manager.read_settings()
        )

        if not result["success"]:

            return result

        destination_path = (
            result["data"]["destination_path"]
        )

        return Result.success(
            data={
                "destination_path":
                    destination_path,
            }
        )

    def set_destination(
        self,
        destination_path,
    ):

        validation = (
            self.validate_destination(
                destination_path
            )
        )

        if not validation["success"]:

            return validation

        result = (
            self.settings_manager.set_destination_path(
                destination_path
            )
        )

        if not result["success"]:

            return result

        return Result.success(
            data={
                "destination_path":
                    str(destination_path),
                "ready_for_backup":
                    True,
            }
        )

    def reset_destination(self):

        result = (
            self.settings_manager
            .reset_destination_path()
        )

        if not result["success"]:

            return result

        return Result.success(
            data={
                "destination_path":
                    result["data"][
                        "destination_path"
                    ],
            }
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_destination(
        self,
        destination_path=None,
    ):

        try:

            if destination_path is None:

                result = (
                    self.get_destination()
                )

                if not result["success"]:

                    return result

                destination_path = (
                    result["data"][
                        "destination_path"
                    ]
                )

            destination_path = str(
                destination_path
            ).strip()

            if not destination_path:

                return Result.error(
                    "Backup destination is empty."
                )

            destination = Path(
                destination_path
            )

            destination.mkdir(
                parents=True,
                exist_ok=True,
            )

            if not destination.exists():

                return Result.error(
                    "Backup destination does not exist."
                )

            if not destination.is_dir():

                return Result.error(
                    "Backup destination is not a directory."
                )

            if not os.access(
                destination,
                os.W_OK,
            ):

                return Result.error(
                    "Backup destination is not writable."
                )

            test_file = (
                destination
                / self.TEST_FILE_NAME
            )

            try:

                with open(
                    test_file,
                    "w",
                    encoding="utf-8",
                ) as file:

                    file.write(
                        "Sunsoft Backup Agent"
                    )

                if not test_file.exists():

                    return Result.error(
                        "Backup destination write test failed."
                    )

            finally:

                test_file.unlink(
                    missing_ok=True
                )

            usage = shutil.disk_usage(
                destination
            )

            return Result.success(
                data={
                    "destination_path":
                        str(destination),

                    "exists":
                        destination.exists(),

                    "is_directory":
                        destination.is_dir(),

                    "writable":
                        True,

                    "free_space":
                        usage.free,

                    "total_space":
                        usage.total,

                    "used_space":
                        usage.used,

                    "ready_for_backup":
                        True,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    # ---------------------------------------------------------
    # Backup Copy
    # ---------------------------------------------------------

    def create_destination_directory(
        self,
        destination_path,
    ):

        destination_directory = Path(
            destination_path
        )

        destination_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return destination_directory

    def _build_destination_filename(
        self,
        source_file: Path,
    ) -> str:

        file_name = source_file.stem

        if "_" in file_name:

            file_name = file_name.rsplit(
                "_",
                1,
            )[0]

        return f"{file_name}.zip"

    def copy_backup(
        self,
        source_file,
        destination_path=None,
    ):

        try:

            source_file = Path(
                source_file
            )

            if not source_file.exists():

                return Result.error(
                    "Source backup file does not exist."
                )

            if not source_file.is_file():

                return Result.error(
                    "Source backup is not a file."
                )

            if source_file.stat().st_size == 0:

                return Result.error(
                    "Source backup file is empty."
                )

            if destination_path is None:

                destination_result = (
                    self.get_destination()
                )

                if not destination_result[
                    "success"
                ]:

                    return destination_result

                destination_path = (
                    destination_result[
                        "data"
                    ][
                        "destination_path"
                    ]
                )

            validation = (
                self.validate_destination(
                    destination_path
                )
            )

            if not validation["success"]:

                return validation

            destination_directory = (
                self.create_destination_directory(
                    destination_path
                )
            )

            destination_file = (
                destination_directory
                / self._build_destination_filename(
                    source_file
                )
            )

            temp_name = (
                destination_file.stem
                + "."
                + uuid.uuid4().hex
                + ".new.zip"
            )

            temp_destination = (
                destination_directory
                / temp_name
            )

            source_size = (
                source_file.stat().st_size
            )

            shutil.copy2(
                source_file,
                temp_destination,
            )

            if not temp_destination.exists():

                return Result.error(
                    "Failed to copy backup."
                )

            destination_size = (
                temp_destination.stat().st_size
            )

            if destination_size != source_size:

                temp_destination.unlink(
                    missing_ok=True
                )

                return Result.error(
                    "Backup copy verification failed."
                )

            if destination_size == 0:

                temp_destination.unlink(
                    missing_ok=True
                )

                return Result.error(
                    "Copied backup is empty."
                )

            temp_destination.replace(
                destination_file
            )

            if not destination_file.exists():

                return Result.error(
                    "Backup destination file was not created."
                )

            final_size = (
                destination_file.stat().st_size
            )

            if final_size != source_size:

                return Result.error(
                    "Final backup verification failed."
                )

            return Result.success(
                data={
                    "status": "SUCCESS",

                    "source_file":
                        str(source_file),

                    "destination_path":
                        str(destination_directory),

                    "destination_file":
                        str(destination_file),

                    "source_size":
                        source_size,

                    "destination_size":
                        final_size,

                    "copy_success":
                        True,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )