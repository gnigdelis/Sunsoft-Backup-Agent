import subprocess


class WindowsServiceManager:

    def __init__(self):

        pass

    def get_all_services(self):

        try:

            result = subprocess.run(

                [

                    "powershell",

                    "-Command",

                    "Get-Service | Select-Object Name,Status"

                ],

                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",

            )

            return result.stdout

        except Exception:

            return ""

    def service_exists(
        self,
        service_name: str,
    ):

        services = self.get_all_services()

        return service_name in services

    def service_is_running(
        self,
        service_name: str,
    ):

        services = self.get_all_services()

        if service_name not in services:

            return False

        for line in services.splitlines():

            if service_name in line:

                return "Running" in line

        return False

    def get_service_information(
        self,
        service_name: str,
    ):

        return {

            "exists":

                self.service_exists(
                    service_name
                ),

            "running":

                self.service_is_running(
                    service_name
                ),

        }