import os
import zipfile

from core.common.result import Result


class CompressionEngine:

    def compress_folder(

        self,
        source_folder,
        zip_file_path,

    ):

        try:

            with zipfile.ZipFile(

                zip_file_path,
                "w",
                zipfile.ZIP_DEFLATED,

            ) as zip_file:

                for root, dirs, files in os.walk(

                    source_folder,

                ):

                    for file in files:

                        file_path = os.path.join(

                            root,
                            file,

                        )

                        archive_name = os.path.relpath(

                            file_path,
                            source_folder,

                        )

                        zip_file.write(

                            file_path,
                            archive_name,

                        )

            size_mb = round(

                os.path.getsize(
                    zip_file_path
                ) / (1024 * 1024),

                2,

            )

            return Result.success(

                data={

                    "zip_file":

                        zip_file_path,

                    "compressed_size_mb":

                        size_mb,

                }

            )

        except Exception as error:

            return Result.error(

                str(error)

            )