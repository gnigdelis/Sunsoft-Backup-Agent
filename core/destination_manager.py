from pathlib import Path
import shutil

from core.common.result import Result


class DestinationManager:

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

    def copy_backup(
        self,
        source_file,
        destination_path,
    ):

        try:

            destination_directory = (
                self.create_destination_directory(
                    destination_path
                )
            )

            source_file = Path(
                source_file
            )

            destination_file = (
                destination_directory
                / source_file.name
            )

            shutil.copy2(
                source_file,
                destination_file,
            )

            success = (
                destination_file.exists()
            )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "source_file": str(source_file),
                    "destination_file": str(
                        destination_file
                    ),
                    "copy_success": success,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )