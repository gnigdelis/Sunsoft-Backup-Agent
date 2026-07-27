import os
import shutil

from core.common.result import Result


class SettingsBackupManager:

    SOURCE_PATH = (
        r"C:\ProgramData\Technoran"
        r"\Samtec Next A\Settings"
    )

    DESTINATION_PATH = (
        "temp/settings"
    )

    def backup_settings(self):

        try:

            if not os.path.exists(
                self.SOURCE_PATH
            ):

                return Result.error(
                    "Ο φάκελος Settings δεν βρέθηκε."
                )

            if os.path.exists(
                self.DESTINATION_PATH
            ):

                shutil.rmtree(
                    self.DESTINATION_PATH
                )

            shutil.copytree(
                self.SOURCE_PATH,
                self.DESTINATION_PATH,
            )

            return Result.success(

                data={

                    "source":
                        self.SOURCE_PATH,

                    "destination":
                        self.DESTINATION_PATH,

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )