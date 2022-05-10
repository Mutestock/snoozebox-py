from pathlib import Path


SNOOZEFILE_DEFAULT_CONTENTS = """"
[services]
[options]
schematics_path = "schematics"
"""


def generate_snoozefile(path: Path = None):
    if not path:
        path = "snoozefile.toml"

    with open(path, "rw") as file_handler:
        if not file_handler.readlines():
            file_handler.write(SNOOZEFILE_DEFAULT_CONTENTS)
        else:
            print("snoozefile was not empty. Won't write stuff on it")
