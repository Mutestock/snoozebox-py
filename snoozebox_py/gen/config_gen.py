from typing import List
from utils.pathing import (
    get_relative_generated_config_file,
)
import rtoml
from pipe import select



def dict_recurse_define(base: dict, keys: List[str]) -> None:
    key_to_append = keys[0]
    if not base.get(key_to_append):
        base[key_to_append] = {}
    del keys[0]
    if len(keys) > 0:
        dict_recurse_define(base=base[key_to_append], keys=keys)

IRRELEVANT_CONFIG_KEYS: dict = {
    "postgres": [],
    "redis": [],
    "cassandra": [],
    "mongodb": [],
    "grpc": [],
    "rest": [],
    "kafka": [],
    "rabbitmq": [],
}

BASE_IRRELEVANT_CONFIG_KEYS: list = ["dependencies", "debian_dependencies"]


def write_config(config: dict) -> None:
    service: str = config["service"].lower()
    database: str = config["database"].lower()
    def mode_write(config: dict, mode: str) -> None:
        dict_recurse_define(
            config, ["relative_config_toml", mode, "database", database]
        )
        dict_recurse_define(config, ["relative_config_toml", mode, "service", service])
        dict_recurse_define(config, ["relative_config_toml", mode, "database", "redis"])
        settings: dict = config["settings"]
        
        config["relative_config_toml"][mode]["database"][database] = settings["database"][database]
        config["relative_config_toml"][mode]["database"]["redis"] = settings["database"]["redis"]
        config["relative_config_toml"][mode]["service"][service] = settings["server"][service]
        
        for db in [database, "redis"]:
            for key in BASE_IRRELEVANT_CONFIG_KEYS + IRRELEVANT_CONFIG_KEYS.get(db):
                config["relative_config_toml"][mode]["database"][db].pop(key, None)
        for key in BASE_IRRELEVANT_CONFIG_KEYS + IRRELEVANT_CONFIG_KEYS.get(service):
            config["relative_config_toml"][mode]["service"][service].pop(key, None)
        
        
    list(["local", "test"] | select(lambda x: mode_write(config, x)))
    rtoml.dump(pretty=True, file=open(get_relative_generated_config_file(config), "w"), obj=config["relative_config_toml"])
