import os
import platform

import psutil


class SystemDiscovery:

    def __init__(self):

        pass

    def get_computer_name(self):

        return platform.node()

    def get_current_user(self):

        return os.getlogin()

    def get_windows_version(self):

        return platform.platform()

    def get_cpu(self):

        return platform.processor()

    def get_total_ram(self):

        total_ram = psutil.virtual_memory().total

        return round(
            total_ram / (1024 ** 3),
            2,
        )

    def get_total_disk_space(self):

        total_disk = psutil.disk_usage("C:\\").total

        return round(
            total_disk / (1024 ** 3),
            2,
        )

    def get_free_disk_space(self):

        free_disk = psutil.disk_usage("C:\\").free

        return round(
            free_disk / (1024 ** 3),
            2,
        )

    def discover(self):

        return {

            "success": True,

            "message": "System Discovery completed successfully.",

            "data": {

                "computer_name":
                    self.get_computer_name(),

                "current_user":
                    self.get_current_user(),

                "windows_version":
                    self.get_windows_version(),

                "cpu":
                    self.get_cpu(),

                "ram":
                    f"{self.get_total_ram()} GB",

                "total_disk":
                    f"{self.get_total_disk_space()} GB",

                "free_disk":
                    f"{self.get_free_disk_space()} GB",

            }

        }