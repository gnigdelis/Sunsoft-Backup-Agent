class DeleteMyDataResponse:

    name = "Delete MyDATA Response"

    def get_sql(self):

        return """
        DELETE FROM TblSnMyDATA_Response
        WHERE MyDATA_ResponseStatusCode <> 'Success'
        """