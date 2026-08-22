class ShrinkDatabase:

    name = "Shrink Database"

    def get_sql(self):

        return """

        DBCC SHRINKDATABASE (0,10)

        """