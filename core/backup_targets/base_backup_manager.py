from core.common.result import Result


class BaseBackupManager:

    def __init__(self, events=None):

        self.events = events

    #
    # INFO
    #

    def info(self, message):

        if self.events:

            self.events.log_info.emit(message)

    #
    # SUCCESS
    #

    def success(self, message):

        if self.events:

            self.events.log_success.emit(message)

    #
    # ERROR
    #

    def error(self, message):

        if self.events:

            self.events.log_error.emit(message)

    #
    # RESULT HELPERS
    #

    def ok(self, data=None):

        return Result.success(data=data)

    def fail(self, message):

        self.error(message)

        return Result.error(message)