from typing import Dict, List
from utils.pathing import (
    PathingManager,
)
import rtoml
from pipe import select



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

BASE_IRRELEVANT_CONFIG_KEYS: List = ["dependencies", "debian_dependencies"]


def write_config(config: Dict) -> None:
    """Writes the relevant configuration values to the generated config.toml file

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """    
    service: str = config["service"].lower()
    database: str = config["database"].lower()
    generated_toml: Dict = {}
    def mode_write(config: Dict, mode: str) -> None:
        dict_recurse_define(
            generated_toml, [mode, "database", database]
        )
        dict_recurse_define(generated_toml, [ mode, "service", service])
        dict_recurse_define(generated_toml, [ mode, "database", "redis"])
        settings: Dict = config["settings"]
        
        generated_toml[mode]["database"][database] = settings["database"][database]
        generated_toml[mode]["database"]["redis"] = settings["database"]["redis"]
        generated_toml[mode]["service"][service] = settings["server"][service]
        
        for db in [database, "redis"]:
            for key in BASE_IRRELEVANT_CONFIG_KEYS + IRRELEVANT_CONFIG_KEYS.get(db):
                generated_toml[mode]["database"][db].pop(key, None)
        for key in BASE_IRRELEVANT_CONFIG_KEYS + IRRELEVANT_CONFIG_KEYS.get(service):
            generated_toml[mode]["service"][service].pop(key, None)
        
        
    list(["local", "test"] | select(lambda x: mode_write(config, x)))
    rtoml.dump(pretty=True, file=open(PathingManager().generated_config, "w"), obj=generated_toml)