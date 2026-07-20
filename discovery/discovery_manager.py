from core.installation_snapshot import (
    InstallationSnapshot,
)


class DiscoveryManager:

    def start_discovery(
        self,
    ) -> InstallationSnapshot:

        snapshot = InstallationSnapshot()

        #
        # STEP 1
        # Installation Discovery
        #

        self.discover_installation(
            snapshot
        )

        #
        # STEP 2
        # Configuration Discovery
        #

        self.discover_configuration_files(
            snapshot
        )

        #
        # STEP 3
        # Database Discovery
        #

        self.discover_databases(
            snapshot
        )

        #
        # STEP 4
        # Discovery Completed
        #

        snapshot.discovery_completed = True

        return snapshot


    def discover_installation(
        self,
        snapshot,
    ):

        pass


    def discover_configuration_files(
        self,
        snapshot,
    ):

        pass


    def discover_databases(
        self,
        snapshot,
    ):

        pass