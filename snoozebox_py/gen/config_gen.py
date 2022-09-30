from typing import Dict, List
from utils.pathing import (
    PathingManager,
)
import rtoml
from pipe import select
from copy import copy, deepcopy


def dict_recurse_define(base: Dict, keys: List[str]) -> None:
    """Recursively define dictionary key-value pairs with empty values.
    This is generally to make things cleaner when defining configuration values for rtoml generation.

    :param base: Dictionary to recurse
    :type base: Dict
    :param keys: Keys to populate with empty values.
    :type keys: List[str]
    """
    key_to_append = keys[0]
    if not base.get(key_to_append):
        base[key_to_append] = {}
    del keys[0]
    if len(keys) > 0:
        dict_recurse_define(base=base[key_to_append], keys=keys)


IRRELEVANT_CONFIG_KEYS: Dict = {
    "postgres": [],
    "redis": [],
    "cassandra": [],
    "mongodb": [],
    "grpc": [],
    "rest": [],
    "kafka": [],
    "rabbitmq": [],
}

BASE_IRRELEVANT_CONFIG_KEYS: List = [
    "dependencies",
    "debian_dependencies",
    "default_port",
]


def write_config(config: Dict) -> None:
    """Writes the relevant configuration values to the generated config.toml file

    :param config: Configuration dictionary which gets passed around and modified duruing the generation process
    :type config: Dict
    """
    service: str = config["service"].lower()
    database: str = config["database"].lower()
    generated_toml: Dict = {}
    default_port: int = config["settings"]["database"][database]["default_port"]
    default_redis_port: int = config["settings"]["database"]["redis"]["default_port"]
    docker_compose_redis_name: str = f"{config['project_name']}_cache"
    docker_compose_database_name: str = f"{config['project_name']}_{database.lower()}"

    def mode_write(config: Dict, generated_toml: dict, mode: str) -> None:
        dict_recurse_define(generated_toml, [mode, "database", database])
        dict_recurse_define(generated_toml, [mode, "service", service])
        dict_recurse_define(generated_toml, [mode, "database", "redis"])
        settings: Dict = copy(config["settings"])

        generated_toml[mode]["database"][database] = settings["database"][database]
        generated_toml[mode]["database"]["redis"] = settings["database"]["redis"]
        generated_toml[mode]["service"][service] = settings["server"][service]

        for db in [database, "redis"]:
            for key in BASE_IRRELEVANT_CONFIG_KEYS + IRRELEVANT_CONFIG_KEYS.get(db):
                generated_toml[mode]["database"][db].pop(key, None)
        for key in BASE_IRRELEVANT_CONFIG_KEYS + IRRELEVANT_CONFIG_KEYS.get(service):
            generated_toml[mode]["service"][service].pop(key, None)

    list(
        ["local", "test", "production"]
        | select(lambda x: mode_write(copy(config), generated_toml, x))
    )

    set_production_specific_settings(
        generated_toml,
        database,
        default_port,
        default_redis_port,
        docker_compose_redis_name,
        docker_compose_database_name,
    )

    rtoml.dump(
        pretty=True,
        file=open(PathingManager().generated_config, "w"),
        obj=generated_toml,
    )


def set_production_specific_settings(
    generated_toml: dict,
    database: str,
    default_port: int,
    default_redis_port: int,
    docker_compose_redis_name: str,
    docker_compose_database_name: str,
):

    production = deepcopy(generated_toml["production"])
    production["database"][database]["port"] = default_port
    production["database"][database]["host"] = docker_compose_database_name
    production["database"]["redis"]["port"] = default_redis_port
    production["database"]["redis"]["host"] = docker_compose_redis_name
    generated_toml["production"] = deepcopy(production)
