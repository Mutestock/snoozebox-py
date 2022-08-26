from pathlib import Path
from typing import List
import rtoml

from utils.pathing import PathingManager


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

    contents = {}
    contents["services"] = {}
    contents["occupied_ports"] = []
    contents["options"] = {}
    contents["schematics_path"] = "schematics"

    with open(path, "r") as file_reader:
        if not file_reader.readlines():
            with open(path, "w") as file_writer:
                file_writer.write(SNOOZEFILE_DEFAULT_CONTENTS)
        else:
            print("snoozefile was not empty. Won't write stuff on it")


def get_occupied_ports() -> list:
    toml_contents: dict = rtoml.load(PathingManager().snoozefile)
    return toml_contents["services"]["occupied_ports"]


def mark_ports_occupied(ports: List[str]) -> None:
    toml_contents: dict = rtoml.load(open(PathingManager().snoozefile, "r"))
    occupied_ports: list = toml_contents["services"]["occupied_ports"]
    occupied_ports += ports
    toml_contents["services"]["occupied_ports"] = occupied_ports
    rtoml.dump(
        pretty=True, file=open(PathingManager().snoozefile, "w"), obj=toml_contents
    )


def shift_configured_ports_by_snoozefile(config: dict) -> None:
    occupied_ports: list = get_occupied_ports()
    occupied_ports.sort(reverse=True)
    service: str = config["service"].lower()
    db: str = config["database"].lower()

    if occupied_ports:
        highest_port: int = occupied_ports[0]

        new_service_port: int = highest_port + 1
        new_db_port: int = highest_port + 2
        new_redis_port: int = highest_port + 3

        config["settings"]["server"][service]["port"] = new_service_port
        config["settings"]["database"][db]["port"] = new_db_port
        config["settings"]["database"]["redis"]["port"] = new_redis_port

    mark_ports_occupied(
        [
            config["settings"]["server"][service]["port"],
            config["settings"]["database"][db]["port"],
            config["settings"]["database"]["redis"]["port"],
        ]
    )
