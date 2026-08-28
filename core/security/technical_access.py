from PySide6.QtCore import QObject, Signal
import hashlib
import os


class TechnicalAccess(QObject):

    access_changed = Signal(bool)

    _unlocked = False
    _instance = None

    def __init__(self):

        if getattr(
            self,
            "_initialized",
            False,
        ):
            return

        super().__init__()

        self._initialized = True

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(
                cls
            )

        return cls._instance

    @classmethod
    def verify_password(
        cls,
        password,
    ):

        configured_password = os.environ.get(
            "SUNSOFT_TECHNICAL_PASSWORD",
            "Sun$0ft",
        )

        if not password:

            return False

        password_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        configured_hash = hashlib.sha256(
            configured_password.encode("utf-8")
        ).hexdigest()

        return password_hash == configured_hash

    @classmethod
    def unlock(
        cls,
        password,
    ):

        if not cls.verify_password(
            password
        ):

            return False

        cls._unlocked = True

        cls().access_changed.emit(
            True
        )

        return True

    @classmethod
    def lock(cls):

        cls._unlocked = False

        cls().access_changed.emit(
            False
        )

    @classmethod
    def is_unlocked(cls):

        return cls._unlocked