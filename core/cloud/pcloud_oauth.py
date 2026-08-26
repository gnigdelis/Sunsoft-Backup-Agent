import json
import os
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.request import Request
from urllib.request import urlopen


from core.common.result import Result


class PCloudOAuth:

    AUTHORIZATION_URL = (
        "https://my.pcloud.com/oauth2/authorize"
    )

    DEFAULT_TOKEN_HOSTNAME = (
        "api.pcloud.com"
    )

    REDIRECT_HOST = (
        "127.0.0.1"
    )

    REDIRECT_PORT = 8765

    REDIRECT_PATH = (
        "/pcloud/callback"
    )

    TOKEN_DIRECTORY = (
        Path.home()
        / "AppData"
        / "Local"
        / "Sunsoft"
        / "BackupAgent"
    )

    TOKEN_FILE = (
        TOKEN_DIRECTORY
        / "pcloud_token.json"
    )

    def __init__(
        self,
        client_id=None,
        client_secret=None,
    ):

        self.client_id = (
            client_id
            or os.environ.get(
                "SUNSOFT_PCLOUD_CLIENT_ID"
            )
        )

        self.client_secret = (
            client_secret
            or os.environ.get(
                "SUNSOFT_PCLOUD_CLIENT_SECRET"
            )
        )

        self.redirect_uri = (
            f"http://"
            f"{self.REDIRECT_HOST}:"
            f"{self.REDIRECT_PORT}"
            f"{self.REDIRECT_PATH}"
        )

        self._server = None

        self._callback_thread = None

        self._authorization_code = None

        self._authorization_error = None

        self._authorization_hostname = None

        self._authorization_location_id = None

        self._authorization_uid = None

        self._state = None

    # ==========================================================
    # CONFIGURATION
    # ==========================================================

    def is_configured(self):

        return bool(
            self.client_id
        )

    # ==========================================================
    # CONNECTION
    # ==========================================================

    def is_connected(self):

        token = (
            self.load_token()
        )

        if not token:

            return False

        return bool(
            token.get(
                "access_token"
            )
        )

    # ==========================================================
    # AUTHORIZATION URL
    # ==========================================================

    def get_authorization_url(self):

        if not self.client_id:

            return Result.error(
                "Δεν έχει οριστεί το pCloud Client ID."
            )

        self._state = (
            secrets.token_urlsafe(32)
        )

        parameters = {

            "client_id":
                self.client_id,

            "response_type":
                "code",

            "redirect_uri":
                self.redirect_uri,

            "state":
                self._state,

        }

        authorization_url = (

            self.AUTHORIZATION_URL
            + "?"
            + urlencode(
                parameters
            )

        )

        return Result.success(

            data={

                "authorization_url":
                    authorization_url,

                "state":
                    self._state,

                "redirect_uri":
                    self.redirect_uri,

            }

        )

    # ==========================================================
    # START AUTHORIZATION
    # ==========================================================

    def start_authorization(self):

        result = (
            self.get_authorization_url()
        )

        if not result["success"]:

            return result

        self._authorization_code = None

        self._authorization_error = None

        self._authorization_hostname = None

        self._authorization_location_id = None

        self._authorization_uid = None

        try:

            self._server = (
                self._create_callback_server()
            )

        except Exception as error:

            return Result.error(
                str(error)
            )

        self._callback_thread = (
            threading.Thread(

                target=(
                    self._run_callback_server
                ),

                daemon=True,

            )
        )

        self._callback_thread.start()

        authorization_url = (
            result["data"][
                "authorization_url"
            ]
        )

        try:

            opened = (
                webbrowser.open(
                    authorization_url
                )
            )

            if not opened:

                self._shutdown_server()

                return Result.error(
                    "Δεν ήταν δυνατό να ανοίξει ο browser."
                )

        except Exception as error:

            self._shutdown_server()

            return Result.error(
                str(error)
            )

        return Result.success(

            data={

                "authorization_url":
                    authorization_url,

                "redirect_uri":
                    self.redirect_uri,

                "state":
                    self._state,

            }

        )

    # ==========================================================
    # WAIT FOR CALLBACK
    # ==========================================================

    def wait_for_callback(
        self,
        timeout=300,
    ):

        if not self._server:

            return Result.error(
                "Ο OAuth server δεν έχει ξεκινήσει."
            )

        callback_thread = (
            self._callback_thread
        )

        if callback_thread:

            callback_thread.join(
                timeout
            )

        if self._authorization_error:

            return Result.error(
                self._authorization_error
            )

        if not self._authorization_code:

            return Result.error(
                "Δεν λήφθηκε authorization code."
            )

        return Result.success(

            data={

                "code":
                    self._authorization_code,

                "hostname":
                    self._authorization_hostname,

                "locationid":
                    self._authorization_location_id,

                "uid":
                    self._authorization_uid,

            }

        )

    # ==========================================================
    # TOKEN EXCHANGE
    # ==========================================================

    def exchange_code_for_token(
        self,
        authorization_code,
        hostname=None,
        location_id=None,
        uid=None,
    ):

        if not self.client_id:

            return Result.error(
                "Δεν έχει οριστεί το pCloud Client ID."
            )

        if not self.client_secret:

            return Result.error(
                "Δεν έχει οριστεί το pCloud Client Secret."
            )

        api_hostname = (
            hostname
            or
            self.DEFAULT_TOKEN_HOSTNAME
        )

        api_hostname = (
            api_hostname
            .replace(
                "https://",
                ""
            )
            .replace(
                "http://",
                ""
            )
            .rstrip("/")
        )

        token_url = (
            f"https://"
            f"{api_hostname}"
            f"/oauth2_token"
        )

        parameters = {

            "client_id":
                self.client_id,

            "client_secret":
                self.client_secret,

            "code":
                authorization_code,

        }

        try:

            response = (
                self._post_json(
                    token_url,
                    parameters,
                )
            )

            if response.get(
                "result"
            ) != 0:

                error_message = (
                    response.get(
                        "error"
                    )
                    or
                    "Το pCloud απέρριψε το authorization code."
                )

                return Result.error(
                    str(error_message)
                )

            access_token = (
                response.get(
                    "access_token"
                )
            )

            if not access_token:

                return Result.error(
                    "Το pCloud δεν επέστρεψε access token."
                )

            token = {

                "access_token":
                    access_token,

                "token_type":
                    response.get(
                        "token_type",
                        "bearer",
                    ),

                "uid":
                    response.get(
                        "uid",
                        uid,
                    ),

                "hostname":
                    api_hostname,

                "locationid":
                    response.get(
                        "locationid",
                        location_id,
                    ),

            }

            save_result = (
                self.save_token(
                    token
                )
            )

            if not save_result["success"]:

                return save_result

            return Result.success(

                data={

                    "connected":
                        True,

                    "hostname":
                        api_hostname,

                    "locationid":
                        token.get(
                            "locationid"
                        ),

                    "uid":
                        token.get(
                            "uid"
                        ),

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    # ==========================================================
    # COMPLETE CONNECTION
    # ==========================================================

    def connect(self):

        if not self.is_configured():

            return Result.error(
                "Το pCloud Client ID δεν έχει ρυθμιστεί."
            )

        start_result = (
            self.start_authorization()
        )

        if not start_result["success"]:

            return start_result

        callback_result = (
            self.wait_for_callback()
        )

        if not callback_result["success"]:

            return callback_result

        callback_data = (
            callback_result[
                "data"
            ]
        )

        code = (
            callback_data[
                "code"
            ]
        )

        hostname = (
            callback_data.get(
                "hostname"
            )
        )

        location_id = (
            callback_data.get(
                "locationid"
            )
        )

        uid = (
            callback_data.get(
                "uid"
            )
        )

        return (
            self.exchange_code_for_token(

                authorization_code=code,

                hostname=hostname,

                location_id=location_id,

                uid=uid,

            )
        )

    # ==========================================================
    # TOKEN STORAGE
    # ==========================================================

    def save_token(
        self,
        token,
    ):

        try:

            self.TOKEN_DIRECTORY.mkdir(

                parents=True,

                exist_ok=True,

            )

            temporary_file = (
                self.TOKEN_FILE.with_suffix(
                    ".tmp"
                )
            )

            with open(

                temporary_file,

                "w",

                encoding="utf-8",

            ) as token_file:

                json.dump(

                    token,

                    token_file,

                    indent=4,

                )

            os.replace(

                temporary_file,

                self.TOKEN_FILE,

            )

            return Result.success(

                data={

                    "token_file":
                        str(
                            self.TOKEN_FILE
                        ),

                }

            )

        except Exception as error:

            return Result.error(
                str(error)
            )

    def load_token(self):

        try:

            if not self.TOKEN_FILE.exists():

                return None

            with open(

                self.TOKEN_FILE,

                "r",

                encoding="utf-8",

            ) as token_file:

                return json.load(
                    token_file
                )

        except Exception:

            return None

    def clear_token(self):

        try:

            if self.TOKEN_FILE.exists():

                self.TOKEN_FILE.unlink()

            return Result.success()

        except Exception as error:

            return Result.error(
                str(error)
            )

    def get_token(self):

        token = (
            self.load_token()
        )

        if not token:

            return Result.error(
                "Δεν υπάρχει αποθηκευμένη σύνδεση pCloud."
            )

        if not token.get(
            "access_token"
        ):

            return Result.error(
                "Το αποθηκευμένο pCloud token δεν είναι έγκυρο."
            )

        return Result.success(
            data=token
        )

    # ==========================================================
    # CALLBACK SERVER
    # ==========================================================

    def _create_callback_server(self):

        oauth = self

        class CallbackHandler(
            BaseHTTPRequestHandler
        ):

            def do_GET(self):

                parsed_url = (
                    urlparse(
                        self.path
                    )
                )

                if (
                    parsed_url.path
                    != oauth.REDIRECT_PATH
                ):

                    self.send_response(
                        404
                    )

                    self.end_headers()

                    return

                parameters = (
                    parse_qs(
                        parsed_url.query
                    )
                )

                state = (
                    parameters
                    .get(
                        "state",
                        [None]
                    )[0]
                )

                code = (
                    parameters
                    .get(
                        "code",
                        [None]
                    )[0]
                )

                error = (
                    parameters
                    .get(
                        "error",
                        [None]
                    )[0]
                )

                hostname = (
                    parameters
                    .get(
                        "hostname",
                        [None]
                    )[0]
                )

                location_id = (
                    parameters
                    .get(
                        "locationid",
                        [None]
                    )[0]
                )

                uid = (
                    parameters
                    .get(
                        "uid",
                        [None]
                    )[0]
                )

                if state != oauth._state:

                    oauth._authorization_error = (
                        "Το OAuth state δεν είναι έγκυρο."
                    )

                elif error:

                    oauth._authorization_error = (
                        f"pCloud OAuth error: {error}"
                    )

                elif not code:

                    oauth._authorization_error = (
                        "Το pCloud δεν επέστρεψε authorization code."
                    )

                else:

                    oauth._authorization_code = (
                        code
                    )

                    oauth._authorization_hostname = (
                        hostname
                    )

                    oauth._authorization_location_id = (
                        location_id
                    )

                    oauth._authorization_uid = (
                        uid
                    )

                self.send_response(
                    200
                )

                self.send_header(

                    "Content-Type",

                    "text/html; "
                    "charset=utf-8",

                )

                self.end_headers()

                response_html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>
                        Sunsoft Backup Agent
                    </title>
                </head>
                <body>
                    <h2>
                        Sunsoft Backup Agent
                    </h2>
                    <p>
                        Η σύνδεση με το pCloud ολοκληρώθηκε.
                    </p>
                    <p>
                        Μπορείτε να κλείσετε αυτό το παράθυρο.
                    </p>
                </body>
                </html>
                """

                self.wfile.write(
                    response_html.encode(
                        "utf-8"
                    )
                )

                threading.Thread(

                    target=(
                        oauth._shutdown_server
                    ),

                    daemon=True,

                ).start()

            def log_message(
                self,
                format,
                *args,
            ):

                return

        server = HTTPServer(

            (
                self.REDIRECT_HOST,

                self.REDIRECT_PORT,

            ),

            CallbackHandler,

        )

        return server

    def _run_callback_server(self):

        try:

            self._server.serve_forever()

        except Exception as error:

            if not self._authorization_code:

                self._authorization_error = (
                    str(error)
                )

    def _shutdown_server(self):

        server = self._server

        if not server:

            return

        try:

            server.shutdown()

        except Exception:

            pass

        try:

            server.server_close()

        except Exception:

            pass

        self._server = None

    # ==========================================================
    # HTTP HELPERS
    # ==========================================================

    @staticmethod
    def _post_json(
        url,
        parameters,
    ):

        body = urlencode(
            parameters
        ).encode(
            "utf-8"
        )

        request = Request(

            url,

            data=body,

            method="POST",

        )

        request.add_header(

            "Content-Type",

            "application/x-www-form-urlencoded",

        )

        request.add_header(

            "Accept",

            "application/json",

        )

        with urlopen(

            request,

            timeout=30,

        ) as response:

            response_body = (
                response.read()
                .decode(
                    "utf-8"
                )
            )

        return json.loads(
            response_body
        )