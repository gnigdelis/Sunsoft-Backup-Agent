from __future__ import annotations

from pathlib import Path

from core.common.hash_utils import HashUtils
from core.common.result import Result
from core.manifest.manifest_builder import ManifestBuilder
from core.manifest.manifest_reader import ManifestReader
from core.manifest.manifest_validator import ManifestValidator
from core.manifest.manifest_writer import ManifestWriter


class ManifestEngine:

    def __init__(self):

        self._builder = ManifestBuilder()

        self._writer = ManifestWriter()

        self._reader = ManifestReader()

        self._validator = ManifestValidator()

    # ---------------------------------------------------------

    def create(
        self,
        *,
        output_file: str | Path,
        zip_file: str | Path,
        application_name: str,
        application_version: str,
        backup_type: str,
        duration_seconds: float = 0,
        database_server: str = "",
        database_name: str = "",
        database_engine: str = "",
        targets: list | None = None,
    ) -> Result:

        try:

            zip_path = Path(zip_file)

            manifest = self._builder.build(

                application_name=application_name,

                application_version=application_version,

                backup_type=backup_type,

                database_server=database_server,

                database_name=database_name,

                database_engine=database_engine,

                targets=targets,

            )

            manifest["backup"][
                "duration_seconds"
            ] = duration_seconds

            manifest["archive"] = {

                "file":
                    zip_path.name,

                "size":
                    zip_path.stat().st_size,

                "sha256":
                    HashUtils.sha256(
                        zip_path
                    ),

            }

            return self._writer.write(

                manifest=manifest,

                output_file=output_file,

            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    # ---------------------------------------------------------

    def read(
        self,
        manifest_file: str | Path,
    ) -> Result:

        return self._reader.read(
            manifest_file
        )

    # ---------------------------------------------------------

    def validate(
        self,
        manifest: dict,
    ) -> Result:

        return self._validator.validate(
            manifest
        )

    # ---------------------------------------------------------

    def load_and_validate(
        self,
        manifest_file: str | Path,
    ) -> Result:

        read_result = self.read(
            manifest_file
        )

        if not read_result["success"]:

            return read_result

        validation = self.validate(

            read_result["data"]

        )

        if not validation["success"]:

            return validation

        return Result.success(

            data=read_result["data"]

        )