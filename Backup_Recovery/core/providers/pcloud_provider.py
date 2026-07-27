import os

from core.common.result import Result


class PCloudProvider:

    def validate_path(

        self,
        destination_path,

    ):

        try:

            os.makedirs(

                destination_path,
                exist_ok=True,

            )

            writable = os.access(

                destination_path,
                os.W_OK,

            )

            return Result.success(

                data={

                    "destination_path":

                        destination_path,

                    "exists":

                        os.path.exists(
                            destination_path
                        ),

                    "writable":

                        writable,

                    "ready_for_backup":

                        writable,

                }

            )

        except Exception as error:

            return Result.error(

                str(error)

            )