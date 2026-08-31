from pathlib import Path
import sys


def resource_path(*parts) -> str:
    """
    Return an absolute path to a bundled resource.

    Works both:
      - from source
      - from PyInstaller one-file executable
    """

    if getattr(
        sys,
        "frozen",
        False,
    ):

        base_path = Path(
            getattr(
                sys,
                "_MEIPASS",
                Path(sys.executable).resolve().parent,
            )
        )

    else:

        # core/common/resource_path.py
        # -> project root is two levels above this file.
        base_path = Path(
            __file__
        ).resolve().parents[2]

    return str(
        base_path.joinpath(
            *parts
        )
    )
