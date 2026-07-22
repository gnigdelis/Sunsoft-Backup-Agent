import os


def ensure_directory_exists(

    directory_path,

):

    os.makedirs(

        directory_path,
        exist_ok=True,

    )

    return directory_path