import platform
import shutil

import psutil


class SystemInformation:

    @staticmethod
    def get_computer_name():

        return platform.node()

    @staticmethod
    def get_windows_version():

        return platform.platform()

    @staticmethod
    def get_processor():

        processor = platform.processor()

        if not processor:

            return "Δεν βρέθηκε"

        return processor

    @staticmethod
    def get_ram():

        ram = psutil.virtual_memory().total

        ram_gb = round(
            ram / (1024 ** 3),
            2,
        )

        return f"{ram_gb} GB"

    @staticmethod
    def get_free_disk_space():

        total, used, free = shutil.disk_usage(
            "C:\\"
        )

        free_gb = round(
            free / (1024 ** 3),
            2,
        )

        return f"{free_gb} GB"