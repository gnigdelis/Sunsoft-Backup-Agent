from dataclasses import dataclass, field

from core.module_snapshot import ModuleSnapshot
from core.database_snapshot import DatabaseSnapshot


@dataclass
class InstallationSnapshot:

    # ==========================================================
    # INSTALLATION INFORMATION
    # ==========================================================

    installation_found: bool = False

    installation_paths: list[str] = field(
        default_factory=list
    )

    # ==========================================================
    # MODULES
    # ==========================================================

    installed_modules: list[ModuleSnapshot] = field(
        default_factory=list
    )

    # ==========================================================
    # CONFIGURATION FILES
    # ==========================================================

    configuration_files: list = field(
        default_factory=list
    )

    critical_files: list = field(
        default_factory=list
    )

    important_files: list = field(
        default_factory=list
    )

    unknown_files: list = field(
        default_factory=list
    )

    # ==========================================================
    # DATABASE INFORMATION
    # ==========================================================

    database_found: bool = False

    database_type: str = ""

    database_server: str = ""

    database_name: str = ""

    databases: list[DatabaseSnapshot] = field(
        default_factory=list
    )

    # ==========================================================
    # SERVICES INFORMATION
    # ==========================================================

    services_found: list = field(
        default_factory=list
    )

    # ==========================================================
    # REGISTRY INFORMATION
    # ==========================================================

    registry_keys: list = field(
        default_factory=list
    )

    # ==========================================================
    # BACKUP STATUS
    # ==========================================================

    backup_ready: bool = False

    backup_warnings: list = field(
        default_factory=list
    )

    # ==========================================================
    # HEALTH STATUS
    # ==========================================================

    health_status: str = "UNKNOWN"

    # ==========================================================
    # DISCOVERY STATUS
    # ==========================================================

    discovery_completed: bool = False