
import json
import os


class RegistryCollector:

    def export_json(

        self,
        data,
        output_folder,

    ):

        os.makedirs(

            output_folder,
            exist_ok=True,

        )

        output_path = os.path.join(

            output_folder,
            "registry_information.json",

        )

        with open(

            output_path,
            "w",
            encoding="utf-8",

        ) as file:

            json.dump(

                data,
                file,
                indent=4,
                ensure_ascii=False,

            )

        return output_path