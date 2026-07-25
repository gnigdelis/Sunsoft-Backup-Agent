from core.common.result import Result


class HealthCheckManager:

    def __init__(self):

        self.score = 100

        self.warnings = []

        self.errors = []

        self.recommendations = []

    def add_warning(

        self,
        message,

    ):

        self.score -= 5

        self.warnings.append(
            message
        )

    def add_error(

        self,
        message,

    ):

        self.score -= 10

        self.errors.append(
            message
        )

    def add_recommendation(

        self,
        message,

    ):

        self.recommendations.append(
            message
        )

    def get_health_score(self):

        return max(
            self.score,
            0,
        )

    def ready_for_backup(self):

        return len(
            self.errors
        ) == 0

    def get_result(self):

        return Result.success(

            data={

                "health_score":

                    self.get_health_score(),

                "ready_for_backup":

                    self.ready_for_backup(),

                "warnings":

                    self.warnings,

                "errors":

                    self.errors,

                "recommendations":

                    self.recommendations,

            }

        )