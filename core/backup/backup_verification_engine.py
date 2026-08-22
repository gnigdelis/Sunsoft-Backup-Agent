from __future__ import annotations

from pathlib import Path

from core.backup.backup_verification_result import (
    BackupVerificationResult,
)

from core.common.hash_utils import (
    HashUtils,
)

from core.common.result import (
    Result,
)

from core.manifest.manifest_engine import (
    ManifestEngine,
)


class BackupVerificationEngine:

    def __init__(self):

        self._manifest_engine = ManifestEngine()

    # ---------------------------------------------------------

    def verify(
        self,
        backup_folder: str | Path,
    ) -> Result:

        try:

            backup_folder = Path(backup_folder)

            verification = BackupVerificationResult()

            manifest_file = (
                backup_folder /
                "backup_manifest.json"
            )

            if manifest_file.exists():

                verification.manifest_exists = True

            else:

                verification.add_error(
                    "Το backup_manifest.json δεν βρέθηκε."
                )

                return Result.success(
                    data=verification
                )

            read_result = (
                self._manifest_engine
                .load_and_validate(
                    manifest_file
                )
            )

            if not read_result["success"]:

                verification.add_error(
                    "Το Manifest δεν είναι έγκυρο."
                )

                verification.metadata = {
                    "details": read_result["errors"]
                }

                return Result.success(
                    data=verification
                )

            verification.manifest_valid = True

            manifest = read_result["data"]

            archive = manifest.get(
                "archive",
                {}
            )

            zip_name = archive.get(
                "file",
                ""
            )

            if not zip_name:

                verification.add_error(
                    "Το Manifest δεν περιέχει όνομα ZIP."
                )

                verification.metadata = manifest

                return Result.success(
                    data=verification
                )

            zip_file = (
                backup_folder /
                zip_name
            )

            if not zip_file.exists():

                verification.add_error(
                    "Το ZIP του backup δεν βρέθηκε."
                )

                verification.metadata = manifest

                return Result.success(
                    data=verification
                )

            verification.zip_exists = True

            # ---------------------------------------------
            # SHA256 Verification
            # ---------------------------------------------

            expected_sha = archive.get(
                "sha256",
                ""
            )

            actual_sha = HashUtils.sha256(
                zip_file
            )

            if expected_sha:

                if expected_sha == actual_sha:

                    verification.checksum_valid = True

                else:

                    verification.add_error(
                        "Το SHA256 του backup δεν συμφωνεί."
                    )

            else:

                verification.add_warning(
                    "Δεν υπάρχει SHA256 στο Manifest."
                )

            # ---------------------------------------------
            # File Size Verification
            # ---------------------------------------------

            expected_size = archive.get(
                "size",
                0
            )

            actual_size = zip_file.stat().st_size

            if expected_size:

                if expected_size == actual_size:

                    verification.size_valid = True

                else:

                    verification.add_error(
                        "Το μέγεθος του ZIP δεν συμφωνεί."
                    )

            else:

                verification.add_warning(
                    "Δεν υπάρχει μέγεθος ZIP στο Manifest."
                )

            verification.metadata = manifest

            return Result.success(
                data=verification
            )

        except Exception as error:

            return Result.error(
                str(error)
            )