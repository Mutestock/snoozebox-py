DATABASE_OPTIONS: dict = {"1": "Postgres", "2": "MongoDB", "3": "Cassandra"}
SERVICE_OPTIONS: dict = {"1": "Rest", "2": "gRPC", "3": "Kafka", "4": "RabbitMQ"}
from gen import gen_base
from utils.config import CONFIG
import sys

def run_append_prompt(config: dict = None) -> dict:
    if not config:
        config: dict = {}
    print("Welcome to snoozebox")
    print("\nNote that poetry is required: https://python-poetry.org/")
    print("\nPlease type the project's name")
    config["project_name"] = input()
    if not config['project_name']:
        sys.exit("The project name can't be empty")
    _database_prompt(config)
    _service_prompt(config)
    config.update(CONFIG)
    return config
    


def _database_prompt(config: dict) -> None:

    print("Please choose a database paradigm")
    _print_options(DATABASE_OPTIONS)
    selected_database = input()
    config = _manage_selection(DATABASE_OPTIONS, config, selected_database, "database")    
    if not config:
        _database_prompt()


def _service_prompt(config: dict) -> None:

    print("Please select a service type:")
    _print_options(SERVICE_OPTIONS)
    selected_service_type = input()
    config = _manage_selection(
        SERVICE_OPTIONS, config, selected_service_type, "service"
    )
    if not config:
        _service_prompt()
        


def _print_options(options: dict) -> None:
    for key, value in options.items():
        print(key + ". " + value)
    print(f"Type 1-{ len(options.values()) }")


def _manage_selection(
    options: dict, config: dict, selection: str, subject: str
) -> dict:
    
    if not selection.isnumeric():
        print(selection + " is not a number. Please try again")
        return
    elif (int(selection) > len(options.values()) + 1) or (int(selection) <= 0):
        print("Input not recognized. Try again")
        return _manage_selection(options, config, selection, subject)
    else:
        config[subject] = options.get(selection)
        return config
