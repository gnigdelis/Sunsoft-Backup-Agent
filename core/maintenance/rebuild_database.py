class RebuildDatabase:

    name = "Rebuild Database"

    def get_sql(self):

        return """
        EXEC SPSnRebuildUpdate
        """