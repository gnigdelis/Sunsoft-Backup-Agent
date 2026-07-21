import psutil


class DatabaseDiscovery:

    def __init__(self):

        pass

    def get_sql_services(self):

        sql_services = []

        try:

            for service in psutil.win_service_iter():

                service_information = service.as_dict()

                service_name = service_information.get(
                    "name",
                    ""
                )

                #
                # SQL SERVER SERVICES
                #

                if (

                    service_name.upper().startswith(
                        "MSSQL"
                    )

                    or

                    service_name.upper().startswith(
                        "SQL"
                    )

                ):

                    sql_services.append(

                        {

                            "service_name":
                                service_information.get(
                                    "name"
                                ),

                            "display_name":
                                service_information.get(
                                    "display_name"
                                ),

                            "status":
                                service_information.get(
                                    "status"
                                ),

                            "start_type":
                                service_information.get(
                                    "start_type"
                                ),

                        }

                    )

        except Exception as error:

            return {

                "success": False,

                "message": str(error),

                "data": []

            }

        return {

            "success": True,

            "message": "SQL Services discovered successfully.",

            "data": sql_services,

        }

    def discover(self):

        sql_result = self.get_sql_services()

        return {

            "success": sql_result["success"],

            "message": sql_result["message"],

            "data": {

                "sql_services_found":

                    len(
                        sql_result["data"]
                    ),

                "services":

                    sql_result["data"]

            }

        }