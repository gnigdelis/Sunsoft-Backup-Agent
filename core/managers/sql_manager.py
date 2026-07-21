import json

from pathlib import Path

from core.windows.service_manager import (
    WindowsServiceManager,
)


class SQLManager:

    def __init__(self):

        self.service_manager = (
            WindowsServiceManager()
        )

    def get_supported_sql_services(self):

        settings_path = Path(

            "settings",
            "database",
            "supported_sql_services.json",

        )

        with open(
            settings_path,
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

    def get_sql_services(self):

        sql_services = []

        for service_name in (

            self.get_supported_sql_services()

        ):

            information = (

                self.service_manager
                .get_service_information(
                    service_name
                )

            )

            if information["exists"]:

                sql_services.append(

                    {

                        "name":
                            service_name,

                        "running":
                            information[
                                "running"
                            ],

                    }

                )

        return sql_services

    def sql_exists(self):

        return len(

            self.get_sql_services()

        ) > 0

    def get_running_sql_services(self):

        return [

            service

            for service in

            self.get_sql_services()

            if service["running"]

        ]

    def get_sql_information(self):

        services = (

            self.get_sql_services()

        )

        return {

            "sql_found":

                self.sql_exists(),

            "total_services":

                len(
                    services
                ),

            "running_services":

                len(
                    self.get_running_sql_services()
                ),

            "services":

                services,

        }