from core.cleanup_manager import (
    CleanupManager,
)

from core.paths import (
    Paths,
)


class BackupEngine:

    def execute(self):

        try:

            #
            # CLEAN TEMP
            #

            CleanupManager.cleanup_temp_folder()

            #
            # CREATE TEMP FOLDERS
            #

            Paths.get_files_folder()
            Paths.get_sql_folder()
            Paths.get_registry_folder()
            Paths.get_programdata_folder()

            return {

                "success": True,

                "message":

                    "Backup Engine initialized successfully.",

            }

        except Exception as error:

            return {

                "success": False,

                "message":

                    str(error),

            }