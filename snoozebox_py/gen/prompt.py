from pathlib import Path
from utils.config import CONFIG
import sys
from pipe import select
from snoozelib import sql_tables_to_classes
from utils.pathing import PathingManager, get_directories_with_sql_files

DATABASE_OPTIONS: dict = {"1": "Postgres", "2": "MongoDB", "3": "Cassandra"}
SERVICE_OPTIONS: dict = {"1": "Rest", "2": "gRPC", "3": "Kafka", "4": "RabbitMQ"}


def run_append_prompt(config: dict = None) -> dict:
    if not config:
        config: dict = {}
    config.update(CONFIG)
    print("Welcome to snoozebox")
    print("\nNote that poetry is required: https://python-poetry.org/")
    print("\nPlease type the project's name")
    config["project_name"] = input()
    if not config["project_name"]:
        sys.exit("The project name can't be empty")
    PathingManager(config)
    if Path(PathingManager().project_root).is_dir():
        sys.exit("A directory with this name already exists")
    _database_prompt(config)
    _service_prompt(config)
    print("Grabbing schematics...")
    schematics = _grab_schematics()
    _schematics_prompt(config, schematics)
    config["schematics"] = list(
        config["schematics_directory"]
        | select(lambda x: sql_tables_to_classes(open(x, "r").read()))
    )
    return config


def _database_prompt(config: dict) -> None:

    print("Please choose a database paradigm\n")
    _print_options(DATABASE_OPTIONS)
    selected_database = input()
    intermediate_config = _manage_selection(DATABASE_OPTIONS, config, selected_database, "database")
    if not intermediate_config:
        _database_prompt(config)
    else:
        config = intermediate_config


def _service_prompt(config: dict) -> None:

    print("Please select a service type:\n")
    _print_options(SERVICE_OPTIONS)
    selected_service_type = input()
    intermediate_config = _manage_selection(
        SERVICE_OPTIONS, config, selected_service_type, "service"
    )
    if not intermediate_config:
        _service_prompt(config)
    else:
        config = intermediate_config


def _schematics_prompt(config: dict, schematics: dict) -> None:

    print(
        "These are the directories in the schematics directory which contain sql files"
    )
    print("Select one\n")
    enumerated: dict = {}
    for i, (key, value) in enumerate(schematics.items()):
        i_mod = str(i + 1)
        print(f"{i_mod}. {key}")
        enumerated[i_mod] = value
    selected_schematic = input()
    print(selected_schematic)
    intermediate_config = _manage_selection(
        enumerated, config, selected_schematic, "schematics_directory"
    )
    if not intermediate_config:
        _schematics_prompt(config, schematics)
    else:
        config = intermediate_config


def _print_options(options: dict) -> None:
    for key, value in options.items():
        print(key + ". " + value)
    print(f"Type 1-{ len(options.values()) }\n")


def _manage_selection(
    options: dict, config: dict, selection: str, subject: str
) -> dict:

    if not selection.isnumeric():
        print(selection + " is not a number. Please try again")
        return
    elif (int(selection) > len(options.values())) or (int(selection) <= 0):
        print("Please select a number inside the specified range.")
        return
    else:
        config[subject] = options.get(selection)
        return config


def _grab_schematics() -> dict:
    sql_dict = get_directories_with_sql_files(PathingManager().init_root / "schematics")
    if not sql_dict:
        print("No schematics found during execution")
        sys.exit("Aborting due to missing schematics...")
    return sql_dict
