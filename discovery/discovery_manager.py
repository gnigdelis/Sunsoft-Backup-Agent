from core.installation_snapshot import InstallationSnapshot

from installation.installation_manager import (
    installation_exists,
    discover_installation_paths,
    discover_modules,
)

from configuration.configuration_manager import (
    discover_configuration_files,
)


class DiscoveryManager:

    def __init__(self):

        self.snapshot = InstallationSnapshot()

    def start_discovery(self):

        print()
        print("=" * 60)
        print("SUNSOFT BACKUP AGENT - DISCOVERY ENGINE")
        print("=" * 60)
        print()

        print("Starting Discovery Engine...")
        print()

        self.run_installation_discovery()

        self.run_configuration_discovery()

        self.snapshot.discovery_completed = True

        print()
        print("Discovery Engine completed successfully.")
        print()

        return self.snapshot

    def run_installation_discovery(self):

        print("Running Installation Discovery...")
        print()

        self.snapshot.installation_found = (
            installation_exists()
        )

        self.snapshot.installation_paths = (
            discover_installation_paths()
        )

        self.snapshot.installed_modules = (
            discover_modules()
        )

        print(
            f"Installation Found : "
            f"{self.snapshot.installation_found}"
        )

        print()

        print("Installation Paths")
        print("-" * 60)

        for path in self.snapshot.installation_paths:

            print(path)

        print()

        print("Installed Modules")
        print("-" * 60)

        for module in self.snapshot.installed_modules:

            print()

            print(
                f"Module Name      : "
                f"{module.module_name}"
            )

            print(
                f"Program Files    : "
                f"{module.has_program_files}"
            )

            print(
                f"Program Data     : "
                f"{module.has_program_data}"
            )

        print()

    def run_configuration_discovery(self):

        print("Running Configuration Discovery...")
        print()

        configuration_files = (
            discover_configuration_files()
        )

        self.snapshot.configuration_files = (
            configuration_files
        )

        print(
            f"Configuration Files Found : "
            f"{len(configuration_files)}"
        )

        print()