import os
import platform
import shutil

from core.common.result import Result


class SystemInformationManager:

    def get_system_information(self):

        try:

            computer_name = platform.node()

            operating_system = (
                f"{platform.system()} "
                f"{platform.release()}"
            )

            cpu_information = (
                platform.processor()
            )

            total_ram_gb = (
                round(
                    os.sysconf(
                        "SC_PAGE_SIZE"
                    )
                    * os.sysconf(
                        "SC_PHYS_PAGES"
                    )
                    / (1024 ** 3),
                    2,
                )
                if hasattr(
                    os,
                    "sysconf"
                )
                else "Unknown"
            )

            disk_usage = shutil.disk_usage(
                "C:\\"
            )

            total_disk_gb = round(
                disk_usage.total / (1024 ** 3),
                2,
            )

            free_disk_gb = round(
                disk_usage.free / (1024 ** 3),
                2,
            )

            return Result.success(
                data={
                    "computer_name":
                        computer_name,

                    "operating_system":
                        operating_system,

                    "cpu_information":
                        cpu_information,

                    "total_ram_gb":
                        total_ram_gb,

                    "total_disk_gb":
                        total_disk_gb,

                    "free_disk_gb":
                        free_disk_gb,

                    "status":
                        "SUCCESS",
                }
            )

        except Exception as error:

            return Result.error(
                str(error)
            )