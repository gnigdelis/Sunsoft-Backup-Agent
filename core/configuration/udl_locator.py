from pathlib import Path


class UDLLocator:

    SEARCH_PATHS = [

        Path(
            r"C:\ProgramData\Sunsoft\BackOffice"
        ),

        Path(
            r"C:\ProgramData\Sunsoft"
        ),

        Path(
            r"C:\Program Files (x86)\Sunsoft Ltd"
        ),

        Path(
            r"C:\Program Files\Sunsoft Ltd"
        ),

    ]

    @classmethod
    def find_all(cls):

        found = []

        for root in cls.SEARCH_PATHS:

            if not root.exists():
                continue

            for udl in root.rglob("*.udl"):

                udl = udl.resolve()

                if udl not in found:

                    found.append(
                        udl
                    )

        return found

    @classmethod
    def find(cls) -> str:

        #
        # First try the selected database.
        #

        from core.database.database_context import (
            database_context
        )

        active_udl = database_context.active_udl()

        if active_udl:

            return active_udl

        #
        # Backwards compatibility.
        #
        # If no database has been selected yet,
        # use Initial.udl as before.
        #

        for udl in cls.find_all():

            if udl.name.lower() == "initial.udl":

                return str(udl)

        raise FileNotFoundError(
            "No UDL file was found."
        )