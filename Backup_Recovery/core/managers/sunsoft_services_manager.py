import json
import subprocess


class SunsoftServicesManager:

    def __init__(self):

        pass

    def load_services(self):

        with open(

            "settings/services/supported_services.json",
            "r",
            encoding="utf-8",

        ) as file:

            data = json.load(
                file
            )

        return data.get(
            "services",
            [],
        )

    def service_exists(

        self,
        service_name,

    ):

        try:

            result = subprocess.run(

                [

                    "sc",
                    "query",
                    service_name,

                ],

                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",

            )

            return result.returncode == 0

        except Exception:

            return False

    def service_running(

        self,
        service_name,

    ):

        try:

            result = subprocess.run(

                [

                    "sc",
                    "query",
                    service_name,

                ],

                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",

            )

            return "RUNNING" in result.stdout

        except Exception:

            return False

    def get_information(self):

        services = self.load_services()

        results = []

        warnings = []

        for service in services:

            exists = self.service_exists(
                service["name"]
            )

            running = False

            if exists:

                running = self.service_running(
                    service["name"]
                )

            if service["required"] and not exists:

                warnings.append(

                    f"{service['display_name']} is missing."

                )

            results.append(

                {

                    "service_name":
                        service["name"],

                    "display_name":
                        service["display_name"],

                    "required":
                        service["required"],

                    "exists":
                        exists,

                    "running":
                        running,

                }

            )

        status = "SUCCESS"

        if warnings:

            status = "WARNING"

        return {

            "success": True,

            "status": status,

            "warnings": warnings,

            "errors": [],

            "data": results,

        }