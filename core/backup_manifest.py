import hashlib
import json
import platform
from datetime import datetime
from pathlib import Path

from core.common.result import Result


class BackupManifest:

    VERSION = "1.0"

    def create(
        self,
        session_name: str,
        session_path: str,
        zip_file: str,
        targets: list[str],
    ):

        try:

            zip_path = Path(zip_file)

            manifest = {

                "manifest_version": self.VERSION,

                "created":

                    datetime.now().isoformat(),

                "computer":

                    platform.node(),

                "system":

                    platform.system(),

                "system_version":

                    platform.version(),

                "python_version":

                    platform.python_version(),

                "session_name":

                    session_name,

                "session_path":

                    session_path,

                "zip_file":

                    zip_path.name,

                "zip_size":

                    zip_path.stat().st_size if zip_path.exists() else 0,

                "sha256":

                    self.calculate_sha256(zip_path),

                "targets":

                    targets,

            }

            manifest_file = (
                Path(session_path)
                / "backup_manifest.json"
            )

            with open(
                manifest_file,
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

                    "manifest_file": str(manifest_file),

                }

            )

        except Exception as error:

            return Result.error(str(error))

    # ---------------------------------------------------------

    @staticmethod
    def calculate_sha256(file_path: Path):

        if not file_path.exists():
            return ""

        sha = hashlib.sha256()

        with open(file_path, "rb") as file:

            while True:

                chunk = file.read(65536)

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()