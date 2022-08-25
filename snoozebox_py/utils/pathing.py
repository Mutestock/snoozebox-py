from dataclasses import dataclass
from typing import Dict, List
from typing_extensions import Self
from pipe import select
from pathlib import Path


def create_directories_if_not_exists(directories: List[Path]):
    """Creates directories if they don't already exists

    :param directories: List of Paths to create
    :type directories: List[Path]
    """    
    def _mkdir_if_not_exists(dir: Path):
        Path.mkdir(dir, exist_ok=True)

    list(directories | select(lambda x: _mkdir_if_not_exists(x)))


def create_empty_files_if_not_exists(files: List[Path]):
    """Creates files if they don't already exists

    :param files: List of Paths to files to create
    :type files: List[Path]
    """    
    def _touch_if_not_exists(file_name: Path):
        if not file_name.exists():
            open(file_name, "w").close()

    list(files | select(lambda x: _touch_if_not_exists(x)))


@dataclass(init=False)
class PathingManager():
    """A singleton containing a variety of paths. An alternative to a lazy static. 
    Requires the config file to create, hence can't use normal constants.
    """    
    project_root: Path
    src: Path
    tests: Path
    generated_config: Path
    init_root: Path
    docker_compose: Path
    dockerfile: Path
    _instance = None
    
    def __new__(cls: type[Self], _: Dict = None) -> Self:
        if cls._instance == None:
            cls._instance = super(PathingManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, config: Dict = None):
        if config and not hasattr(self, "project_root"):
            self.project_root = Path(f"{config['settings']['file_structure']['root_services']}/{config['project_name']}")
            self.src = self.project_root / f"{config['project_name']}"
            self.tests = self.project_root / "tests"
            self.generated_config = self.project_root / "config.toml"
            self.init_root = Path(config["settings"]["file_structure"]["root_services"]).parent
            self.docker_compose = self.init_root / "docker-compose.yml"
            self.dockerfile = self.project_root / "Dockerfile"



def create_base_directories(config: Dict) -> None:
    """Creates a set of basic directories as defined inside the default values.

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """    
    create_directories_if_not_exists(
        [
            PathingManager().src/ path_def[1]
            for path_def in config["settings"]["file_structure"][
                "project_directories"
            ].values()
        ]
    )
    create_directories_if_not_exists(
        [
            PathingManager().tests / path_def[1]
            for path_def in config["settings"]["file_structure"][
                "test_directories"
            ].values()
        ]
    )


def create_mode_specific_directories(config: Dict) -> None:
    """Directories to be created which a specific to the technologies selected during prompt

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """    
    directories: List[str] = {
        "rest": [],
        "grpc": [PathingManager().project_root / "proto"],
        "kafka": [],
        "rabbitmq": [],
    }.get(config["service"].lower())
    create_directories_if_not_exists(directories)


def get_directories_with_sql_files(path: Path) -> Dict:
    """Retrieves the directories with data from the schematics folder

    :param path: Path from which the data is retrieved. Schematics
    :type path: Path
    :return: The data from the schematics folder
    :rtype: Dict
    """    
    directories_with_sql: Dict = {}

    for item in path.iterdir():
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
