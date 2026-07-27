import winreg


class ApplicationsManager:

    def __init__(self):

        pass

    def get_installed_applications(self):

        applications = []

        registry_paths = [

            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",

            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",

        ]

        for registry_path in registry_paths:

            try:

                key = winreg.OpenKey(

                    winreg.HKEY_LOCAL_MACHINE,
                    registry_path,

                )

                total_keys = (

                    winreg.QueryInfoKey(
                        key
                    )[0]

                )

                for index in range(total_keys):

                    try:

                        subkey_name = (

                            winreg.EnumKey(
                                key,
                                index,
                            )

                        )

                        subkey = (

                            winreg.OpenKey(
                                key,
                                subkey_name,
                            )

                        )

                        application = {

                            "name":
                                self.get_registry_value(
                                    subkey,
                                    "DisplayName",
                                ),

                            "version":
                                self.get_registry_value(
                                    subkey,
                                    "DisplayVersion",
                                ),

                            "publisher":
                                self.get_registry_value(
                                    subkey,
                                    "Publisher",
                                ),

                            "install_date":
                                self.get_registry_value(
                                    subkey,
                                    "InstallDate",
                                ),

                        }

                        if application["name"]:

                            applications.append(
                                application
                            )

                    except Exception:

                        pass

            except Exception:

                pass

        return applications

    def get_registry_value(

        self,
        key,
        value_name,

    ):

        try:

            return winreg.QueryValueEx(

                key,
                value_name,

            )[0]

        except Exception:

            return ""

    def get_information(self):

        applications = (

            self.get_installed_applications()

        )

        status = "SUCCESS"

        warnings = []

        if len(applications) == 0:

            status = "WARNING"

            warnings.append(

                "No installed applications found."

            )

        return {

            "success": True,

            "status": status,

            "warnings": warnings,

            "errors": [],

            "data": applications,

        }