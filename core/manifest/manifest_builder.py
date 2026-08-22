from __future__ import annotations

import platform
import uuid
from datetime import datetime


class ManifestBuilder:
    """
    Δημιουργεί τη δομή του backup manifest.
    Δεν αποθηκεύει αρχεία και δεν κάνει I/O.
    """

    MANIFEST_VERSION = "2.0"

    def build(
        self,
        *,
        application_name: str,
        application_version: str,
        backup_type: str,
        database_server: str = "",
        database_name: str = "",
        database_engine: str = "",
        targets: list | None = None,
    ) -> dict:

        if targets is None:
            targets = []

        return {

            "manifest_version": self.MANIFEST_VERSION,

            "application": {
                "name": application_name,
                "version": application_version,
            },

            "backup": {
                "id": str(uuid.uuid4()),
                "created": datetime.now().isoformat(),
                "type": backup_type,
                "duration_seconds": 0,
            },

            "system": {
                "computer_name": platform.node(),
                "os": platform.system(),
                "os_version": platform.version(),
                "python_version": platform.python_version(),
            },

            "database": {
                "server": database_server,
                "database": database_name,
                "engine": database_engine,
            },

            "targets": targets,

            "archive": {
                "file": "",
                "size": 0,
                "sha256": "",
            }

        }