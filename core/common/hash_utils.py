from __future__ import annotations

import hashlib
from pathlib import Path


class HashUtils:

    @staticmethod
    def sha256(file_path: str | Path) -> str:

        path = Path(file_path)

        if not path.exists():
            return ""

        sha = hashlib.sha256()

        with path.open("rb") as file:

            while chunk := file.read(1024 * 1024):

                sha.update(chunk)

        return sha.hexdigest()