from pathlib import Path


SNOOZEFILE_DEFAULT_CONTENTS = """"
[services]
# Do not edit this value
occupied_ports=[]

[options]
schematics_path = "schematics"
"""


def generate_snoozefile(path: Path = None):
    if not path:
        path = "snoozefile.toml"

    with open(path, "r") as file_reader:
        if not file_reader.readlines():
            with open(path, "w") as file_writer:
                file_writer.write(SNOOZEFILE_DEFAULT_CONTENTS)
        else:
            print("snoozefile was not empty. Won't write stuff on it")
