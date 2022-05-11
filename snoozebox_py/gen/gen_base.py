from gen.connection import pg_gen, cassandra_gen, mongo_gen, redis_gen
from gen.logic.handlers.relational import (
    generic_tools,
    relational_crud_component,
    relational_utils_component,
)
from gen.service.grpc import grpc_main_gen, grpc_routes_gen


def get_postgres_writers(object_list: list) -> list:
    postgres_writers = [
        pg_gen.PostgresConnection,
        generic_tools.GenericRelationalTools,
        relational_crud_component.RelationalCrudComponent,
        relational_utils_component.RelationalUtilsComponent,
    ]
    return postgres_writers


def get_grpc_writers(object_list: list) -> list:
    grpc_writers = [grpc_main_gen.Grpc, grpc_routes_gen]
    return grpc_writers


def touch_docker(config: dict) -> None:
    print("Touch docker placeholder")


def touch_misc(config: dict) -> None:
    print("Touch misc placeholder")
