from utils.pathing import indent_writer
from typing import List
from gen.block_writer_abstract import BlockWriter
from utils.pathing import (
    get_relative_generated_config_file,
    get_relative_project_src_directory,
)
import rtoml


class ConfigWriter(BlockWriter):
    def write(self, config: dict) -> None:
        project_directories: dict = config["settings"]["file_structure"][
            "project_directories"
        ]
        utils: str = project_directories["utils"][0]
        test_environment_variable: str = config["settings"][
            "test_environment_variable_name"
        ][0]
        config_file_name: str = config["settings"]["file_structure"]["project_files"][
            "config_file"
        ]
        file_writer = open(
            f"{get_relative_project_src_directory(config)}/{utils}/config.py", "w"
        )

        indent_writer(
            lvl=0,
            text=f"""\
            import os
            import toml

            _ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            _ROOT_DIR = os.path.dirname(_ROOT_DIR)

            ROOT_DIR = os.path.dirname(_ROOT_DIR)
            CONFIG_FILE_PATH = ROOT_DIR + "/{config_file_name}.toml"
            LOG_FILE_PATH = ROOT_DIR + "/logs"

            CONFIG = {{}}

            _filename = CONFIG_FILE_PATH
            _content: str = ""

            with open(_filename) as f:
                _content = f.read()

            CONFIG = toml.loads(_content)


            def get_config_with_mode() -> dict:
                # Add more modes here. E.g. production
                if os.getenv("{test_environment_variable}"):
                    print("EXECUTION MODE IS: test")
                    return CONFIG["test"]

                print("EXECUTION MODE IS: local")
                return CONFIG["local"]


            CONFIG = get_config_with_mode()
        """,
            file_writer=file_writer,
        )

    @staticmethod
    def initial_conf_push(config: dict) -> None:
        config["relative_config_toml"] = {}
        config["relative_config_toml"]["test"] = {}
        config["relative_config_toml"]["local"] = {}

    @staticmethod
    def final_conf_toml_gen(config: dict) -> None:
        rtoml.dump(
            config["relative_config_toml"],
            open(f"{get_relative_generated_config_file(config)}", "w"),
            pretty=True,
        )


def dict_recurse_define(base: dict, keys: List[str]) -> None:
    key_to_append = keys[0]
    if not base.get(key_to_append):
        base[key_to_append] = {}
    keys.remove(key_to_append)
    if len(keys) > 0:
        dict_recurse_define(base=base[key_to_append], keys=keys)
