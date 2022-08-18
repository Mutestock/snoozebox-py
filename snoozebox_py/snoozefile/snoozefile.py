from pathlib import Path
import rtoml


SNOOZEFILE_DEFAULT_CONTENTS = """"
[services]
# Do not edit this value
occupied_ports=[]

[options]
schematics_path = "schematics"
"""


def generate_snoozefile(path: Path = None):
    """Generates the snoozefile with some basic information. The snoozefile is necessary to store information between appends, as well as asserting a variety of rules.

    :param path: The path in which the snoozefile should be generated, defaults to None
    :type path: Path, optional
    """    
    if not path:
        path = "snoozefile.toml"

    with open(path, "r") as file_reader:
        if not file_reader.readlines():
            with open(path, "w") as file_writer:
                file_writer.write(SNOOZEFILE_DEFAULT_CONTENTS)
        else:
            print("snoozefile was not empty. Won't write stuff on it")


def check_available_ports():
    pass

