import os
from typing import List
from pipe import select
from pathlib import Path
import textwrap


def create_directories_if_not_exists(directories: list[str]):
    def _mkdir_if_not_exists(dir: str):
        if not os.path.exists(dir):
            os.mkdir(dir)

    list(directories | select(lambda x: _mkdir_if_not_exists(x)))


def create_empty_files_if_not_exists(files: list[str]):
    def _touch_if_not_exists(file_name: str):
        if not os.path.exists(file_name):
            open(file_name, "w").close()

    list(files | select(lambda x: _touch_if_not_exists(x)))


# Just to make code more readable elsewhere
def get_relative_project_root_directory(config: dict) -> str:
    return f"{config['settings']['file_structure']['root_services']}/{config['project_name']}"


def get_relative_project_src_directory(config: dict) -> str:
    return f"{get_relative_project_root_directory(config)}/{config['project_name']}"


def get_relative_tests_directory(config: dict) -> str:
    return get_relative_project_root_directory(config) + "/tests"


def get_relative_generated_config_file(config: dict) -> str:
    return f"{get_relative_project_root_directory(config)}/{config['settings']['file_structure']['project_files']['config_file']}"


def get_parent_of_root_services(config: dict) -> str:
    parent = Path(
        config["settings"]["file_structure"]["root_services"]
    ).parent.absolute()
    return parent


def get_directories_with_sql_files(path_str: str) -> dict:
    directories_with_sql: dict = {}

    for item in Path(path_str).iterdir():
        if item.is_dir():
            for nested_item in item.iterdir():
                if not nested_item.is_file():
                    continue
                if (
                    ".sql" in str(nested_item)
                    or ".json" in str(nested_item)
                    or ".cql" in str(nested_item)
                ):
                    if not directories_with_sql.get(str(item)):
                        directories_with_sql[str(item)] = []
                    directories = directories_with_sql[str(item)]
                    directories.append(str(nested_item))
                    directories_with_sql[str(item)] = directories

    return directories_with_sql


def indent_writer(lvl: int, text: str, file_writer) -> None:
    indent_concat = ""
    for _ in range(lvl):
        indent_concat += " "
    file_writer.write(textwrap.indent(text=textwrap.dedent(text), prefix=indent_concat))
