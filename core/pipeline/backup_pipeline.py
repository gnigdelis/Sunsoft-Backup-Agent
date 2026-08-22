import shutil
import time
from pathlib import Path

from core.backup.settings_backup_manager import SettingsBackupManager
from core.common.result import Result
from core.compression.compression_engine import CompressionEngine
from core.destination.backup_destination_manager import (
    BackupDestinationManager,
)


class BackupPipeline:

    def execute(self) -> Result:

        try:

            start_time = time.perf_counter()

            # -------------------------------------------------
            # Settings Backup
            # -------------------------------------------------

            settings_manager = SettingsBackupManager()

            result = settings_manager.backup_settings()

            if not result.success:
                return result

            # -------------------------------------------------
            # ZIP Compression
            # -------------------------------------------------

            compression_engine = CompressionEngine()

            result = compression_engine.create_backup_zip()

            if not result.success:
                return result

            zip_file = result.data["zip_file"]

            zip_path = Path(zip_file)

            backup_info = {
                "zip_file": zip_file,
                "zip_name": zip_path.name,
                "zip_size": zip_path.stat().st_size,
            }

            # -------------------------------------------------
            # Copy to destination
            # -------------------------------------------------

            destination_manager = BackupDestinationManager()

            result = destination_manager.copy_backup_file(
                zip_file
            )

            if not result.success:
                return result

            # -------------------------------------------------
            # Cleanup
            # -------------------------------------------------

            temp_path = Path("temp")

            if temp_path.exists():

                shutil.rmtree(temp_path)

            # -------------------------------------------------
            # Finish
            # -------------------------------------------------

            elapsed = round(
                time.perf_counter() - start_time,
                2,
            )

            backup_info["duration_seconds"] = elapsed

            return Result.success(
                data={
                    "message": "Το Backup ολοκληρώθηκε επιτυχώς.",
                    "backup": backup_info,
                }
            )

        except Exception as error:

            return Result.error(str(error))