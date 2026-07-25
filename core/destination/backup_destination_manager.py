import os


class BackupDestinationManager:

    DEFAULT_BACKUP_FOLDER = os.path.join(
        os.path.expanduser("~"),
        "SunsoftSupportAgent",
        "Backups",
    )

    @classmethod
    def get_backup_folder(cls):

        cls.create_backup_folder()

        return cls.DEFAULT_BACKUP_FOLDER

    @classmethod
    def create_backup_folder(cls):

        if not os.path.exists(
            cls.DEFAULT_BACKUP_FOLDER
        ):

            os.makedirs(
                cls.DEFAULT_BACKUP_FOLDER,
                exist_ok=True,
            )

    @classmethod
    def backup_folder_exists(cls):

        return os.path.exists(
            cls.DEFAULT_BACKUP_FOLDER
        )

    @classmethod
    def get_total_backups(cls):

        cls.create_backup_folder()

        backups = [

            file

            for file in os.listdir(
                cls.DEFAULT_BACKUP_FOLDER
            )

            if os.path.isfile(

                os.path.join(
                    cls.DEFAULT_BACKUP_FOLDER,
                    file,
                )

            )

        ]

        return len(
            backups
        )