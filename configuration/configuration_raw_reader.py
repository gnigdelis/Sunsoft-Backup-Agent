def read_raw_file(file_path):

    encodings = [

        "utf-8",
        "utf-8-sig",
        "utf-16",
        "latin-1",

    ]

    for encoding in encodings:

        try:

            with open(
                file_path,
                "r",
                encoding=encoding
            ) as file:

                content = file.read()

                if content:

                    return {

                        "success": True,
                        "encoding": encoding,
                        "content": content,

                    }

        except Exception:

            continue

    return {

        "success": False,
        "encoding": None,
        "content": None,

    }