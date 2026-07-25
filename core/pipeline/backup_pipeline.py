import os
import shutil

from core.backup.settings_backup_manager import (
    SettingsBackupManager,
)

from core.compression.compression_engine import (
    CompressionEngine,
)

from core.destination.backup_destination_manager import (
    BackupDestinationManager,
)

from core.common.result import Result


class BackupPipeline:

    def execute(self):

        try:

            # Settings Backup

            settings_manager = (
                SettingsBackupManager()
            )

            result = (
                settings_manager.backup_settings()
            )

            if not result["success"]:

                return result

            # ZIP Compression

            compression_engine = (
                CompressionEngine()
            )

            result = (
                compression_engine.create_backup_zip()
            )

            if not result["success"]:

                return result

            zip_file = (
                result["data"]["zip_file"]
            )

            # Copy to destination

            destination_manager = (
                BackupDestinationManager()
            )

            result = (
                destination_manager.copy_backup_file(
                    zip_file
                )
            )

            if not result["success"]:

                return result

            # Delete temp folder

            if os.path.exists("temp"):

                shutil.rmtree("temp")

            return Result.success(

                data={

                    "message":
                        "Το Backup ολοκληρώθηκε επιτυχώς."

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )