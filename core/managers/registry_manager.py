import json


class RegistryManager:

    def __init__(self):

        pass

    def get_registry_targets(self):

        with open(

            "settings/registry/registry_targets.json",
            "r",
            encoding="utf-8",

        ) as file:

            settings = json.load(
                file
            )

        return settings.get(
            "registry_keys",
            [],
        )

    def get_information(self):

        registry_keys = (
            self.get_registry_targets()
        )

        warnings = []

        status = "SUCCESS"

        if len(registry_keys) == 0:

            status = "WARNING"

            warnings.append(

                "No registry targets configured."

            )

        return {

            "success": True,

            "status": status,

            "warnings": warnings,

            "errors": [],

            "data": registry_keys,

        }