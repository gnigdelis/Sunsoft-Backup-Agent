import json
import os

from pathlib import Path


class ProgramDataManager:

    def __init__(self):

        pass

    def get_targets(self):

        settings_path = Path(

            "settings",
            "programdata",
            "programdata_targets.json",

        )

        with open(

            settings_path,
            "r",
            encoding="utf-8",

        ) as file:

            data = json.load(
                file
            )

        return data.get(
            "targets",
            [],
        )

    def target_exists(
        self,
        path: str,
    ):

        return os.path.exists(
            path
        )

    def get_total_files(
        self,
        path: str,
    ):

        total_files = 0

        for _, _, files in os.walk(
            path
        ):

            total_files += len(
                files
            )

        return total_files

    def get_target_size_mb(
        self,
        path: str,
    ):

        total_size = 0

        for root, _, files in os.walk(
            path
        ):

            for file in files:

                file_path = os.path.join(
                    root,
                    file,
                )

                try:

                    total_size += os.path.getsize(
                        file_path
                    )

                except Exception:

                    pass

        return round(

            total_size / (1024 * 1024),
            2,

        )

    def get_information(self):

        results = []

        for target in self.get_targets():

            path = target["path"]

            exists = self.target_exists(
                path
            )

            information = {

                "name":
                    target["name"],

                "path":
                    path,

                "exists":
                    exists,

                "accessible":
                    exists,

                "total_files":
                    0,

                "size_mb":
                    0,

                "ready_for_backup":
                    False,

            }

            if exists:

                information[
                    "total_files"
                ] = self.get_total_files(
                    path
                )

                information[
                    "size_mb"
                ] = self.get_target_size_mb(
                    path
                )

                information[
                    "ready_for_backup"
                ] = True

            results.append(
                information
            )

        return {

            "success": True,

            "status": "READY",

            "warnings": [],

            "errors": [],

            "data": results,

        }