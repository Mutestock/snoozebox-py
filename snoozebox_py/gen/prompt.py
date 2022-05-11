DATABASE_OPTIONS: dict = {"1": "Postgres", "2": "MongoDB", "3": "Cassandra"}
SERVICE_OPTIONS: dict = {"1": "Rest", "2": "gRPC", "3": "Kafka", "4": "RabbitMQ"}
from gen import gen_base
from utils.config import CONFIG
from utils.poetry_exec import run_poetry

def run_append_prompt(config: dict = None) -> None:
    if not config:
        config: dict = {}
    print("Welcome to snoozebox")
    print("\nNote that poetry is required: https://python-poetry.org/")
    print("\nPlease type the project's name")
    config["project_name"] = input()
    _database_prompt(config)
    _service_prompt(config)
    config.update(CONFIG)    
    writers: list = _populate_generation_writers(config)
    _collect_dependencies(config)
    print("Running Poetry...")
    run_poetry(config)
    print("Writing the specified files...")
    for writer in writers:
        instantiated = writer()
        instantiated.write(config)
        instantiated.write_test(config)
    gen_base.touch_docker(config)
    gen_base.touch_misc(config)
    print("Ok")


def _database_prompt(config: dict) -> None:

    print("Please choose a database paradigm")
    _print_options(DATABASE_OPTIONS)
    selected_database = input()
    config = _manage_selection(DATABASE_OPTIONS, config, selected_database, "database")


def _service_prompt(config: dict) -> None:

    print("Please select a service type:")
    _print_options(SERVICE_OPTIONS)
    selected_service_type = input()
    config = _manage_selection(
        SERVICE_OPTIONS, config, selected_service_type, "service"
    )


def _print_options(options: dict) -> None:
    for key, value in options.items():
        print(key + ". " + value)
    print(f"Type 1-{ len(options.values()) }")


def _manage_selection(
    options: dict, config: dict, selection: str, subject: str
) -> dict:
    try:
        if (int(selection) > len(options.values()) + 1) or (int(selection) <= 0):
            print("Input not recognized. Try again")
            return _manage_selection(config)
        else:
            config[subject] = options.get(selection)
            return config
    except ValueError as e:
        print("Input wasn't a number. Try again. \n")
        return _manage_selection(config)


def _populate_generation_writers(config: dict) -> list:
    writers: list = []
    database: str = config.get("database")
    service: str = config.get("service")
    
    
    # Match hasn't been added in earlier Python versions
    if database == "Postgres":
        writers = writers + gen_base.get_postgres_writers(None)
    elif database == "MongoDB":
        ()
    elif database == "Cassandra":
        ()
    else:
        print("Chosen database wasn't found. This should never happen")
        
    if service == "Rest":
        ()
    elif service == "gRPC":
        writers = writers + gen_base.get_grpc_writers(None)
    elif service == "Kafka":
        ()
    elif service == "RabbitMQ":
        ()
    else:
        print("Chosen service wasn't found. This should never happen")
    
    return writers


def _collect_dependencies(config: dict) -> None:
    database: str = config.get("database")
    service: str = config.get("service")
    dependencies: list = []
    
    # Match hasn't been added in earlier Python versions
    if database == "Postgres":
        dependencies = dependencies + config["settings"]["database"]["postgres"]["dependencies"]
        print("Note: This project uses psycopg2 as its Postgres driver. Secure that the required postgres library is installed on your PC.")
        print("Check https://www.psycopg.org/install/")
    elif database == "MongoDB":
        dependencies = dependencies + config["settings"]["database"]["mongodb"]["dependencies"]
    elif database == "Cassandra":
        dependencies = dependencies + config["settings"]["database"]["cassandra"]["dependencies"]
    else:
        print("Chosen database wasn't found. This should never happen")
        
    if service == "Rest":
        ()
    elif service == "gRPC":
        dependencies = dependencies + config["settings"]["server"]["grpc"]["dependencies"]
    elif service == "Kafka":
        dependencies = dependencies + config["settings"]["server"]["kafka"]["dependencies"]
    elif service == "RabbitMQ":
        dependencies = dependencies + config["settings"]["server"]["rabbitmq"]["dependencies"]
    else:
        print("Chosen service wasn't found. This should never happen")
    
    dependencies = dependencies + config["settings"]["general_dependencies"]
    config["collected_dependencies"] = dependencies
    
    
    