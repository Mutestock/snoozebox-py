import os
from pipe import select


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
def get_relative_project_directory(config: dict) -> str:
    return f"{config['settings']['file_structure']['root_services']}/{config['project_name']}/{config['project_name']}"


def get_relative_tests_directory(config: dict) -> str:
    return f"{config['settings']['file_structure']['root_services']}/{config['project_name']}/tests"
