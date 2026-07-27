import json
import os


class PrinterCollector:

    def __init__(self):

        pass

    def export_json(

        self,
        printers,
        output_folder,

    ):

        os.makedirs(

            output_folder,
            exist_ok=True,

        )

        output_path = os.path.join(

            output_folder,
            "printers.json",

        )

        with open(

            output_path,
            "w",
            encoding="utf-8",

        ) as file:

            json.dump(

                printers,
                file,
                indent=4,
                ensure_ascii=False,

            )

        return output_path