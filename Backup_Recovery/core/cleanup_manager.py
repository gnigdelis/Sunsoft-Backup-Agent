import os
import shutil

from core.paths import (
    Paths,
)


class CleanupManager:

    @staticmethod
    def cleanup_temp_folder():

        temp_folder = (
            Paths.get_temp_folder()
        )

        if os.path.exists(
            temp_folder
        ):

            shutil.rmtree(
                temp_folder,
                ignore_errors=True,
            )

        os.makedirs(
            temp_folder,
            exist_ok=True,
        )

    def delete_directory(
        self,
        directory_path,
    ):

        if not os.path.exists(
            directory_path
        ):

            return

        shutil.rmtree(
            directory_path,
            ignore_errors=True,
        )