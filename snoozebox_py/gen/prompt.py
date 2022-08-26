from pathlib import Path
from typing import Dict, List
from snoozefile.snoozefile import shift_configured_ports_by_snoozefile
from utils.config import CONFIG
import sys
from pipe import select
from snoozelib import sql_tables_to_classes
from utils.pathing import PathingManager, get_directories_with_sql_files

DATABASE_OPTIONS: Dict = {"1": "Postgres", "2": "MongoDB", "3": "Cassandra"}
SERVICE_OPTIONS: Dict = {"1": "Rest", "2": "gRPC", "3": "Kafka", "4": "RabbitMQ"}


def run_append_prompt(config: Dict = None) -> Dict:
    """Executes the prompt which populates the config dictionary with basic information.

    :param config: Configuration dictionary which gets passed around and modified during the generation process, defaults to None
    :type config: Dict, optional
    :return: Configuration dictionary with populated information from the prompt.
    :rtype: Dict
    """

    if not config:
        config: Dict = {}
    config.update(CONFIG)
    print("Welcome to snoozebox")
    print("\nNote that poetry is required: https://python-poetry.org/")
    print("\nPlease type the project's name")
    config["project_name"] = input()
    if not config["project_name"]:
        sys.exit("The project name can't be empty")
    pathing_manager = PathingManager(config)
    if Path(PathingManager().project_root).is_dir():
        sys.exit("A directory with this name already exists")
    _database_prompt(config)
    _service_prompt(config)
    print("Grabbing schematics...")
    schematics = _grab_schematics()
    _schematics_prompt(config, schematics)
    schematics_contents: List[str] = list(
        config["schematics_directory"] | select(lambda x: open(x, "r").read())
    )
    (config["schematics"], config["association_tables"]) = sql_tables_to_classes(schematics_contents)
    shift_configured_ports_by_snoozefile(config)
    return config


def _database_prompt(config: Dict) -> None:
    """Prompts user for database tech selection

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """

    print("Please choose a database paradigm\n")
    _print_options(DATABASE_OPTIONS)
    selected_database = input()
    intermediate_config = _manage_selection(
        DATABASE_OPTIONS, config, selected_database, "database"
    )
    if not intermediate_config:
        _database_prompt(config)
    else:
        config = intermediate_config


def _service_prompt(config: Dict) -> None:
    """Prompts user for service tech selection

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """

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


def _schematics_prompt(config: Dict, schematics: Dict) -> None:
    """Prompts user to choose a directory in the schematics directory for generation

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    :param schematics: The available choices.
    :type schematics: Dict
    """

    print(
        "These are the directories in the schematics directory which contain sql files"
    )
    print("Select one\n")
    enumerated: Dict = {}
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


def _print_options(options: Dict) -> None:
    """Prints the available options to the user. Doesn't target any specific tech. Just prints.

    :param config: The options to print to the terminal.
    :type config: Dict
    """
    for key, value in options.items():
        print(key + ". " + value)
    print(f"Type 1-{ len(options.values()) }\n")


def _manage_selection(
    options: Dict, config: Dict, selection: str, subject: str
) -> Dict:
    """Function which controls the general flow of the selection process.

    :param options: The available options to choose from
    :type options: Dict
    :param config: The options to print to the terminal.
    :type config: Dict
    :param selection: Selected choice. Used as a key with the dictionaries.
    :type selection: str
    :param subject: A key used with the configuration dict. E.g. "database" or "service"
    :type subject: str
    :return: Modified configuration dihighest_port+2ctionary.
    :rtype: Dict
    """

    if not selection.isnumeric():
        print(selection + " is not a number. Please try again")
        return
    elif (int(selection) > len(options.values())) or (int(selection) <= 0):
        print("Please select a number inside the specified range.")
        return
    else:
        config[subject] = options.get(selection)
        return config


def _grab_schematics() -> Dict:
    """Fetches the schematics from the directories which contain data structures

    :return: Data from the data structures
    :rtype: Dict
    """
    sql_dict = get_directories_with_sql_files(PathingManager().init_root / "schematics")
    if not sql_dict:
        print("No schematics found during execution")
        sys.exit("Aborting due to missing schematics...")
    return sql_dict
