import os
import zipfile


class CompressionEngine:

    @staticmethod
    def compress_folder(
        source_folder: str,
        destination_zip_file: str,
    ):

        with zipfile.ZipFile(
            destination_zip_file,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as zip_file:

            for root, _, files in os.walk(
                source_folder
            ):

                for file_name in files:

                    file_path = os.path.join(
                        root,
                        file_name,
                    )

                    archive_name = os.path.relpath(
                        file_path,
                        source_folder,
                    )

                    zip_file.write(
                        file_path,
                        archive_name,
                    )

        return destination_zip_file