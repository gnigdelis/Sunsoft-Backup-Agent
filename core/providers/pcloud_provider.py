import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen

from core.common.result import Result
from core.cloud.pcloud_oauth import PCloudOAuth


class PCloudProvider:

    DEFAULT_BACKUP_FOLDER = (
        "Sunsoft Backup Agent"
    )

    def __init__(self):

        self.oauth = PCloudOAuth()

    def is_connected(self):

        return self.oauth.is_connected()

    def get_connection_status(self):

        token_result = (
            self.oauth.get_token()
        )

        if not token_result["success"]:

            return Result.success(

                data={

                    "connected": False,

                    "message":
                        "Το pCloud δεν είναι συνδεδεμένο.",

                }

            )

        token = (
            token_result["data"]
        )

        return Result.success(

            data={

                "connected": True,

                "hostname":
                    token.get(
                        "hostname"
                    ),

                "message":
                    "Το pCloud είναι συνδεδεμένο.",

            }

        )

    def connect(self):

        return self.oauth.connect()

    def disconnect(self):

        return self.oauth.clear_token()

    def get_token(self):

        return self.oauth.get_token()

    def get_account_info(self):

        token_result = (
            self.oauth.get_token()
        )

        if not token_result["success"]:

            return token_result

        token = (
            token_result["data"]
        )

        hostname = (
            token.get("hostname")
        )

        if not hostname:

            return Result.error(
                "Δεν βρέθηκε pCloud hostname."
            )

        try:

            response = self._api_request(

                hostname,

                "userinfo",

                token,

            )

            if response.get(
                "result"
            ) != 0:

                return Result.error(

                    response.get(
                        "error",
                        "Αποτυχία ανάκτησης στοιχείων pCloud."
                    )

                )

            return Result.success(

                data=response

            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def get_backup_folder(self):

        token_result = (
            self.oauth.get_token()
        )

        if not token_result["success"]:

            return token_result

        token = (
            token_result["data"]
        )

        hostname = (
            token.get("hostname")
        )

        if not hostname:

            return Result.error(
                "Δεν βρέθηκε pCloud hostname."
            )

        try:

            response = self._api_request(

                hostname,

                "listfolder",

                token,

                {

                    "folderid": 0,

                },

            )

            if response.get(
                "result"
            ) != 0:

                return Result.error(

                    response.get(
                        "error",
                        "Αποτυχία ανάγνωσης του pCloud root folder."
                    )

                )

            contents = (
                response.get(
                    "metadata",
                    {}
                ).get(
                    "contents",
                    []
                )
            )

            for item in contents:

                if (
                    item.get("isfolder")
                    and
                    item.get("name")
                    ==
                    self.DEFAULT_BACKUP_FOLDER
                ):

                    return Result.success(

                        data={

                            "folderid":
                                item.get(
                                    "folderid"
                                ),

                            "name":
                                item.get(
                                    "name"
                                ),

                        }

                    )

            return self._create_backup_folder(

                hostname,
                token,

            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def _create_backup_folder(
        self,
        hostname,
        token,
    ):

        try:

            response = self._api_request(

                hostname,

                "createfolder",

                token,

                {

                    "name":
                        self.DEFAULT_BACKUP_FOLDER,

                    "folderid":
                        0,

                },

            )

            if response.get(
                "result"
            ) != 0:

                return Result.error(

                    response.get(
                        "error",
                        "Αποτυχία δημιουργίας pCloud backup folder."
                    )

                )

            metadata = (
                response.get(
                    "metadata",
                    {}
                )
            )

            return Result.success(

                data={

                    "folderid":
                        metadata.get(
                            "folderid"
                        ),

                    "name":
                        metadata.get(
                            "name",
                            self.DEFAULT_BACKUP_FOLDER,
                        ),

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def upload_file(
        self,
        local_file,
        folder_id=None,
    ):

        local_file = Path(
            local_file
        )

        if not local_file.exists():

            return Result.error(

                f"Το αρχείο δεν βρέθηκε: "
                f"{local_file}"

            )

        token_result = (
            self.oauth.get_token()
        )

        if not token_result["success"]:

            return token_result

        token = (
            token_result["data"]
        )

        hostname = (
            token.get("hostname")
        )

        if not hostname:

            return Result.error(
                "Δεν βρέθηκε pCloud hostname."
            )

        if folder_id is None:

            folder_result = (
                self.get_backup_folder()
            )

            if not folder_result["success"]:

                return folder_result

            folder_id = (
                folder_result[
                    "data"
                ][
                    "folderid"
                ]
            )

        try:

            upload_url = (
                f"https://"
                f"{hostname}"
                f"/uploadfile"
            )

            query = urlencode(

                {

                    "access_token":
                        token[
                            "access_token"
                        ],

                    "folderid":
                        folder_id,

                    "filename":
                        local_file.name,

                }

            )

            with open(
                local_file,
                "rb",
            ) as file_handle:

                file_data = (
                    file_handle.read()
                )

            request = Request(

                f"{upload_url}?"
                f"{query}",

                data=file_data,

                method="POST",

            )

            request.add_header(

                "Content-Type",
                "application/octet-stream",

            )

            with urlopen(

                request,
                timeout=300,

            ) as response:

                body = (
                    response.read()
                    .decode(
                        "utf-8"
                    )
                )

            response_data = json.loads(
                body
            )

            if response_data.get(
                "result"
            ) != 0:

                return Result.error(

                    response_data.get(
                        "error",
                        "Αποτυχία upload στο pCloud."
                    )

                )

            return Result.success(

                data={

                    "local_file":
                        str(local_file),

                    "filename":
                        local_file.name,

                    "folderid":
                        folder_id,

                    "response":
                        response_data,

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def validate_connection(self):

        status_result = (
            self.get_connection_status()
        )

        if not status_result["success"]:

            return status_result

        if not status_result[
            "data"
        ][
            "connected"
        ]:

            return Result.error(
                "Το pCloud δεν είναι συνδεδεμένο."
            )

        account_result = (
            self.get_account_info()
        )

        if not account_result["success"]:

            return account_result

        folder_result = (
            self.get_backup_folder()
        )

        if not folder_result["success"]:

            return folder_result

        return Result.success(

            data={

                "connected": True,

                "account":
                    account_result[
                        "data"
                    ],

                "backup_folder":
                    folder_result[
                        "data"
                    ],

            }

        )

    def validate_path(
        self,
        destination_path=None,
    ):

        connection_result = (
            self.validate_connection()
        )

        if not connection_result["success"]:

            return connection_result

        return Result.success(

            data={

                "destination_path":
                    destination_path,

                "connected":
                    True,

                "ready_for_backup":
                    True,

                "backup_folder":
                    connection_result[
                        "data"
                    ][
                        "backup_folder"
                    ],

            }

        )

    @staticmethod
    def _api_request(
        hostname,
        endpoint,
        token,
        parameters=None,
    ):

        parameters = (
            parameters or {}
        )

        parameters = {

            **parameters,

            "access_token":
                token[
                    "access_token"
                ],

        }

        url = (

            f"https://"
            f"{hostname}"
            f"/{endpoint}"
            f"?"
            f"{urlencode(parameters)}"

        )

        request = Request(

            url,
            method="GET",

        )

        with urlopen(

            request,
            timeout=30,

        ) as response:

            body = (
                response.read()
                .decode(
                    "utf-8"
                )
            )

        return json.loads(
            body
        )