from config.critical_files import (
    CRITICAL_FILES,
    IMPORTANT_FILES,
    IGNORED_FILES,
    IGNORED_PATTERNS,
)


def filter_configuration_files(configuration_files):

    critical_files = []
    important_files = []
    ignored_files = []
    unknown_files = []

    for file in configuration_files:

        file_name = file["file_name"]

        #
        # CRITICAL FILES
        #

        if file_name in CRITICAL_FILES:

            critical_files.append(file)
            continue

        #
        # IMPORTANT FILES
        #

        if file_name in IMPORTANT_FILES:

            important_files.append(file)
            continue

        #
        # IGNORED FILES
        #

        if file_name in IGNORED_FILES:

            ignored_files.append(file)
            continue

        #
        # IGNORED PATTERNS
        #

        ignored = False

        for pattern in IGNORED_PATTERNS:

            if file_name.endswith(pattern):

                ignored_files.append(file)

                ignored = True

                break

        if ignored:
            continue

        #
        # UNKNOWN FILES
        #

        unknown_files.append(file)

    return {

        "critical_files": critical_files,
        "important_files": important_files,
        "ignored_files": ignored_files,
        "unknown_files": unknown_files,

    }