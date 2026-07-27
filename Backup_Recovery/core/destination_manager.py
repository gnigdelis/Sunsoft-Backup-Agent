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
                / self._build_destination_filename(
                    source_file
                )
            )

            temp_destination = (
                destination_directory
                / (
                    destination_file.stem
                    + ".new.zip"
                )
            )

            shutil.copy2(
                source_file,
                temp_destination,
            )

            if not temp_destination.exists():

                return Result.error(
                    "Failed to copy backup."
                )

            if (
                temp_destination.stat().st_size
                == 0
            ):

                temp_destination.unlink(
                    missing_ok=True
                )

                return Result.error(
                    "Copied backup is empty."
                )

            temp_destination.replace(
                destination_file
            )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "source_file": str(
                        source_file
                    ),
                    "destination_file": str(
                        destination_file
                    ),
                    "copy_success": destination_file.exists(),
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )