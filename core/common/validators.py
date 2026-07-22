import os


def path_exists(

    path,

):

    return os.path.exists(
        path
    )


def file_exists(

    path,

):

    return os.path.isfile(
        path
    )


def directory_exists(

    path,

):

    return os.path.isdir(
        path
    )