from __future__ import annotations

from core.common.result import Result


class ManifestValidator:
    """
    Ελέγχει την εγκυρότητα ενός Backup Manifest.
    """

    REQUIRED_ROOT_FIELDS = (
        "manifest_version",
        "application",
        "backup",
        "system",
        "database",
        "targets",
        "archive",
    )

    REQUIRED_APPLICATION_FIELDS = (
        "name",
        "version",
    )

    REQUIRED_BACKUP_FIELDS = (
        "id",
        "created",
        "type",
        "duration_seconds",
    )

    REQUIRED_SYSTEM_FIELDS = (
        "computer_name",
        "os",
        "os_version",
        "python_version",
    )

    REQUIRED_DATABASE_FIELDS = (
        "server",
        "database",
        "engine",
    )

    REQUIRED_ARCHIVE_FIELDS = (
        "file",
        "size",
        "sha256",
    )

    def validate(
        self,
        manifest: dict,
    ) -> Result:

        try:

            if not isinstance(manifest, dict):
                return Result.error("Manifest must be a dictionary.")

            # Root fields

            for field in self.REQUIRED_ROOT_FIELDS:

                if field not in manifest:
                    return Result.error(
                        f"Missing root field: {field}"
                    )

            # Application

            result = self._validate_section(
                manifest["application"],
                self.REQUIRED_APPLICATION_FIELDS,
                "application",
            )

            if not result.success:
                return result

            # Backup

            result = self._validate_section(
                manifest["backup"],
                self.REQUIRED_BACKUP_FIELDS,
                "backup",
            )

            if not result.success:
                return result

            # System

            result = self._validate_section(
                manifest["system"],
                self.REQUIRED_SYSTEM_FIELDS,
                "system",
            )

            if not result.success:
                return result

            # Database

            result = self._validate_section(
                manifest["database"],
                self.REQUIRED_DATABASE_FIELDS,
                "database",
            )

            if not result.success:
                return result

            # Archive

            result = self._validate_section(
                manifest["archive"],
                self.REQUIRED_ARCHIVE_FIELDS,
                "archive",
            )

            if not result.success:
                return result

            if not isinstance(manifest["targets"], list):
                return Result.error(
                    "'targets' must be a list."
                )

            return Result.success()

        except Exception as error:

            return Result.error(str(error))

    # ---------------------------------------------------------

    @staticmethod
    def _validate_section(
        section: dict,
        required_fields,
        section_name: str,
    ) -> Result:

        if not isinstance(section, dict):

            return Result.error(
                f"'{section_name}' must be an object."
            )

        for field in required_fields:

            if field not in section:

                return Result.error(
                    f"Missing '{field}' in '{section_name}'."
                )

        return Result.success()