import os
import tempfile


class Paths:

    @staticmethod
    def get_temp_folder():

        temp_folder = os.path.join(

            tempfile.gettempdir(),
            "SunsoftSupportAgent",

        )

        os.makedirs(

            temp_folder,
            exist_ok=True,

        )

        return temp_folder

    @staticmethod
    def get_files_folder():

        folder = os.path.join(

            Paths.get_temp_folder(),
            "Files",

        )

        os.makedirs(

            folder,
            exist_ok=True,

        )

        return folder

    @staticmethod
    def get_sql_folder():

        folder = os.path.join(

            Paths.get_temp_folder(),
            "SQL",

        )

        os.makedirs(

            folder,
            exist_ok=True,

        )

        return folder

    @staticmethod
    def get_registry_folder():

        folder = os.path.join(

            Paths.get_temp_folder(),
            "Registry",

        )

        os.makedirs(

            folder,
            exist_ok=True,

        )

        return folder

    @staticmethod
    def get_programdata_folder():

        folder = os.path.join(

            Paths.get_temp_folder(),
            "ProgramData",

        )

        os.makedirs(

            folder,
            exist_ok=True,

        )

        return folder