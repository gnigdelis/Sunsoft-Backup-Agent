from pathlib import Path
import zipfile

from core.common.result import Result


class ZipCompressionManager:

    def create_zip(
        self,
        source_directory,
        output_directory,
    ):

        try:

            source_directory = Path(
                source_directory
            )

            output_directory = Path(
                output_directory
            )

            output_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            zip_file_path = (
                output_directory
                / f"{source_directory.name}.zip"
            )

            with zipfile.ZipFile(
                zip_file_path,
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
            ) as zip_file:

                for file_path in source_directory.rglob("*"):

                    if file_path.is_file():

                        zip_file.write(
                            file_path,
                            arcname=file_path.relative_to(
                                source_directory
                            ),
                        )

            success = (
                zip_file_path.exists()
            )

            zip_size = (
                zip_file_path.stat().st_size
            )

            return Result.success(
                data={
                    "status": "SUCCESS",
                    "zip_file": str(
                        zip_file_path
                    ),
                    "zip_size": zip_size,
                    "success": success,
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )