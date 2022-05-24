from typing import List
from gen.connection import pg_gen, cassandra_gen, mongo_gen
from gen.logic.handlers.relational import (
    generic_tools,
    relational_crud_component,
    relational_utils_component,
)
from gen.logic.handlers.grpc_handler import GrpcHandler
from gen.service.grpc import grpc_main_gen, grpc_routes_gen
from gen.model.postgres_model import PostgresModelWriter
from gen.protogen import ProtogenWriter
from utils.poetry_exec import run_poetry
from utils.pathing import (
    create_directories_if_not_exists,
    get_relative_project_src_directory,
    get_relative_tests_directory,
)
from gen.config_gen import ConfigWriter
from gen.connection.redis_gen import RedisConnection
from gen.docker_gen import initial_docker_compose_check


def exec_gen(config: dict) -> None:
    writers: list = _populate_generation_writers(config)
    _collect_dependencies(config)

    print("Running Poetry...")
    run_poetry(config)
    print("Making required directories...")
    create_directories_if_not_exists(
        [
            f"{get_relative_project_src_directory(config)}/{path_def[1]}"
            for path_def in config["settings"]["file_structure"][
                "project_directories"
            ].values()
        ]
    )
    create_directories_if_not_exists(
        [
            f"{get_relative_tests_directory(config)}/{path_def[1]}"
            for path_def in config["settings"]["file_structure"][
                "test_directories"
            ].values()
        ]
    )
    print("Writing the specified files...")
    ConfigWriter.initial_conf_push(config)
    initial_docker_compose_check(config)

    for writer in writers:
        instantiated = writer()
        instantiated.write_all(config)
    touch_docker(config)
    touch_misc(config)
    ConfigWriter.final_conf_toml_gen(config)
    print("Ok")


def get_postgres_writers() -> list:
    return [
        pg_gen.PostgresConnection,
        generic_tools.GenericRelationalTools,
        relational_crud_component.RelationalCrudComponent,
        relational_utils_component.RelationalUtilsComponent,
        PostgresModelWriter,
    ]


def get_grpc_writers() -> list:
    return [
        grpc_main_gen.Grpc,
        grpc_routes_gen.GrpcRoutes,
        ProtogenWriter,
        GrpcHandler,
    ]


def get_generic_writers() -> List:
    return [ConfigWriter, RedisConnection]


def touch_docker(config: dict) -> None:
    print("Touch docker placeholder")


def touch_misc(config: dict) -> None:
    print("Touch misc placeholder")


def _populate_generation_writers(config: dict) -> list:
    writers: list = []
    database: str = config["database"]
    service: str = config["service"]
    config["crud_instructions"] = []

    # Match hasn't been added in earlier Python versions
    if database == "Postgres":
        writers = writers + get_postgres_writers()
        config["crud_instructions"] = [
            "create",
            "read",
            "update",
            "delete",
            "read_list",
        ]
    elif database == "MongoDB":
        config["crud_instructions"] = [
            "create",
            "read",
            "update",
            "delete",
            "read_list",
        ]
    elif database == "Cassandra":
        config["crud_instructions"] = [
            "create",
            "read",
            "update",
            "delete",
            "read_list",
        ]
    else:
        print("Chosen database wasn't found. This should never happen")

    if service == "Rest":
        ()
    elif service == "gRPC":
        writers = writers + get_grpc_writers()
    elif service == "Kafka":
        ()
    elif service == "RabbitMQ":
        ()
    else:
        print("Chosen service wasn't found. This should never happen")
    #writers += get_generic_writers()

    return writers


def _collect_dependencies(config: dict) -> None:
    database: str = config.get("database")
    service: str = config.get("service")
    dependencies: list = []

    # Match hasn't been added in earlier Python versions
    if database == "Postgres":
        dependencies = (
            dependencies + config["settings"]["database"]["postgres"]["dependencies"]
        )
        print(
            "Note: This project uses psycopg2 as its Postgres driver. Secure that the required postgres library is installed on your PC."
        )
        print("Check https://www.psycopg.org/install/")
    elif database == "MongoDB":
        dependencies = (
            dependencies + config["settings"]["database"]["mongodb"]["dependencies"]
        )
    elif database == "Cassandra":
        dependencies = (
            dependencies + config["settings"]["database"]["cassandra"]["dependencies"]
        )
    else:
        print("Chosen database wasn't found. This should never happen")

    if service == "Rest":
        ()
    elif service == "gRPC":
        dependencies = (
            dependencies + config["settings"]["server"]["grpc"]["dependencies"]
        )
    elif service == "Kafka":
        dependencies = (
            dependencies + config["settings"]["server"]["kafka"]["dependencies"]
        )
    elif service == "RabbitMQ":
        dependencies = (
            dependencies + config["settings"]["server"]["rabbitmq"]["dependencies"]
        )
    else:
        print("Chosen service wasn't found. This should never happen")

    dependencies = dependencies + config["settings"]["general_dependencies"]
    config["collected_dependencies"] = dependencies
