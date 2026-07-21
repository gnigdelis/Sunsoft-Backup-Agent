class DiscoveryEngine:

    def __init__(self):

        self.results = {

            "system": {},
            "database": {},
            "files": {},
            "registry": {},

            "backup_ready": False,

            "warnings": [],
            "errors": [],

        }

    def run(self):

        """
        Εκτελεί ολόκληρη τη διαδικασία Discovery.
        """

        self.run_system_discovery()

        self.run_database_discovery()

        self.run_files_discovery()

        self.run_registry_discovery()

        self.validate_backup_ready()

        return self.results


    def run_system_discovery(self):

        pass


    def run_database_discovery(self):

        pass


    def run_files_discovery(self):

        pass


    def run_registry_discovery(self):

        pass


    def validate_backup_ready(self):

        """
        Ελέγχει αν το σύστημα είναι
        έτοιμο για Backup.
        """

        pass