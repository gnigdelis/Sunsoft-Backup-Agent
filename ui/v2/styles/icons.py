icons.py"""
Centralized SVG icon definitions.

Never hardcode icon paths in the UI.
Always use Icons.<NAME>.
"""


class Icons:

    # ==========================
    # Navigation
    # ==========================

    DASHBOARD = "navigation/dashboard.svg"
    BACKUP_PAGE = "navigation/backup.svg"
    RESTORE_PAGE = "navigation/restore.svg"
    HISTORY = "navigation/history.svg"
    LOGS = "navigation/logs.svg"
    SETTINGS = "navigation/settings.svg"

    # ==========================
    # Actions
    # ==========================

    BACKUP = "actions/backup.svg"
    UPLOAD = "actions/upload.svg"
    VERIFY = "actions/verify.svg"
    REBUILD = "actions/rebuild.svg"
    DELETE = "actions/delete.svg"

    # ==========================
    # System
    # ==========================

    COMPUTER = "system/computer.svg"
    DATABASE = "system/database.svg"
    STORAGE = "system/storage.svg"

    FILES = "system/files.svg"
    COPIED = "system/copied.svg"
    SPEED = "system/speed.svg"
    CLOCK = "system/clock.svg"

    # ==========================
    # Status
    # ==========================

    SUCCESS = "status/success.svg"
    WARNING = "status/warning.svg"
    ERROR = "status/error.svg"
    INFO = "status/info.svg"