from __future__ import annotations

import json
from pathlib import Path

from core.common.result import Result


class ManifestReader:
    """
    Διαβάζει ένα backup manifest από αρχείο JSON.
    """

    def read(
        self,
        manifest_file: str | Path,
    ) -> Result:

        try:

            manifest_path = Path(manifest_file)

            if not manifest_path.exists():

                return Result.error(
                    f"Manifest file not found: {manifest_path}"
                )

            with manifest_path.open(
                "r",
                encoding="utf-8",
            ) as file:

                manifest = json.load(file)

            return Result.success(
                data=manifest
            )

        except json.JSONDecodeError as error:

            return Result.error(
                f"Invalid JSON: {error}"
            )

        except Exception as error:

            return Result.error(str(error))