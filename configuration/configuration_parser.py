import json

from core.parser_result import ParserResult


def parse_configuration_files(configuration_files):

    parsed_results = []

    for file in configuration_files:

        file_name = file["file_name"]
        file_path = file["full_path"]

        if file_name.endswith(".json"):

            result = parse_json_file(
                file,
                file_path
            )

        elif file_name.endswith(".config"):

            result = parse_text_file(
                file,
                file_path
            )

        else:

            result = ParserResult(
                module_name=file["module_name"],
                file_name=file_name,
                full_path=file_path,
                parse_success=False,
                parse_status="UNSUPPORTED FORMAT",
                parsed_data=None
            )

        parsed_results.append(result)

    return parsed_results


def parse_json_file(file, file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as json_file:

            content = json_file.read()

            if not content.strip():

                return ParserResult(
                    module_name=file["module_name"],
                    file_name=file["file_name"],
                    full_path=file_path,
                    parse_success=False,
                    parse_status="EMPTY FILE",
                    parsed_data=None
                )

            data = json.loads(content)

            return ParserResult(
                module_name=file["module_name"],
                file_name=file["file_name"],
                full_path=file_path,
                parse_success=True,
                parse_status="SUCCESS",
                parsed_data=data
            )

    except json.JSONDecodeError:

        return ParserResult(
            module_name=file["module_name"],
            file_name=file["file_name"],
            full_path=file_path,
            parse_success=False,
            parse_status="INVALID JSON",
            parsed_data=None
        )

    except UnicodeDecodeError:

        return ParserResult(
            module_name=file["module_name"],
            file_name=file["file_name"],
            full_path=file_path,
            parse_success=False,
            parse_status="INVALID ENCODING",
            parsed_data=None
        )

    except Exception:

        return ParserResult(
            module_name=file["module_name"],
            file_name=file["file_name"],
            full_path=file_path,
            parse_success=False,
            parse_status="ACCESS ERROR",
            parsed_data=None
        )


def parse_text_file(file, file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as text_file:

            content = text_file.read()

            if not content.strip():

                return ParserResult(
                    module_name=file["module_name"],
                    file_name=file["file_name"],
                    full_path=file_path,
                    parse_success=False,
                    parse_status="EMPTY FILE",
                    parsed_data=None
                )

            return ParserResult(
                module_name=file["module_name"],
                file_name=file["file_name"],
                full_path=file_path,
                parse_success=True,
                parse_status="SUCCESS",
                parsed_data=content
            )

    except UnicodeDecodeError:

        return ParserResult(
            module_name=file["module_name"],
            file_name=file["file_name"],
            full_path=file_path,
            parse_success=False,
            parse_status="INVALID ENCODING",
            parsed_data=None
        )

    except Exception:

        return ParserResult(
            module_name=file["module_name"],
            file_name=file["file_name"],
            full_path=file_path,
            parse_success=False,
            parse_status="ACCESS ERROR",
            parsed_data=None
        )