import json


def parse_json_file(file_path):

    try:

        with open(
                file_path,
                "r",
                encoding="utf-8"
        ) as file:

            data = json.load(file)

            return data

    except Exception as error:

        print()
        print(f"JSON PARSER ERROR")
        print(error)

        return None