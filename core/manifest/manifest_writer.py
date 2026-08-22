from __future__ import annotations

import json
from pathlib import Path

from core.common.result import Result


class ManifestWriter:
    """
    Αποθηκεύει ένα manifest σε αρχείο JSON.
    """

    def write(
        self,
        manifest: dict,
        output_file: str | Path,
    ) -> Result:

        try:

            output_path = Path(output_file)

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with output_path.open(
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    manifest,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            return Result.success(
                data={
                    "manifest_file": str(output_path)
                }
            )

        except Exception as error:

            return Result.error(str(error))