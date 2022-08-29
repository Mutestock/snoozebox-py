from pathlib import Path
from typing import Dict, List
from jinja2 import Environment
from pipe import where
import subprocess

from .config_gen import write_config
from utils.poetry_exec import run_poetry, poetry_export_requirements
from utils.pathing import (
    create_mode_specific_directories,
    create_base_directories,
    PathingManager,
)
from gen.gitignore_gen import write_git_ignore
from gen.protogen import run_protogen
from gen.template_file_structure import (
    TemplateFileStructure,
    write_templates,
    setup_templating,
)


def templating_generation(jinja_env: Environment = None, config: Dict = None) -> None:
    """Main function for the append generation process.

    :param jinja_env: The environment in which the Jinja should be executed, defaults to None
    :type jinja_env: Environment, optional
    :param config: Configuration dictionary which gets passed around and modified during the generation process, defaults to None
    :type config: Dict, optional
    """

    if not config:
        config: Dict = {}
    if not jinja_env:
        jinja_env: Environment = setup_templating()

    collect_dependencies(config)
    run_poetry(config)
    poetry_export_requirements(config)
    create_base_directories(config)
    create_mode_specific_directories(config)
    _set_crud_instructions(config)
    _run_base_templates(config, jinja_env)
    _run_redis_templates(config, jinja_env)
    _determine_and_run_service_templates(config, jinja_env)
    _determine_and_run_database_templates(config, jinja_env)
    write_git_ignore()
    write_config(config)
    if config["service"].lower() == "grpc":
        run_protogen(config)
    print("Done")


def _determine_and_run_service_templates(config: Dict, jinja_env: Environment) -> None:
    """Checks for the used service types and initiates templates depending on the result.

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    :param jinja_env: The environment in which the Jinja should be executed
    :type jinja_env: Environment
    """
    {
        "rest": _run_rest_templates,
        "grpc": _run_grpc_templates,
        "kafka": None,
        "rabbitmq": None,
    }.get(config["service"].lower())(config, jinja_env)


def _determine_and_run_database_templates(config: Dict, jinja_env: Environment) -> None:
    """Checks for the used database types and initiates templates depending on the result.

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    :param jinja_env: The environment in which the Jinja should be executed
    :type jinja_env: Environment
    """
    {"postgres": _run_pg_templates, "mongodb": None, "cassandra": None}.get(
        config["database"].lower()
    )(config, jinja_env)


def _run_base_templates(config: Dict, jinja_env: Environment) -> None:
    """Runs a set of templates which will always be executed regardless of selected techs

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    :param jinja_env: The environment in which the Jinja should be executed
    :type jinja_env: Environment
    """
    src: Path = PathingManager().src
    docker_compose: Path = PathingManager().docker_compose
    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="misc/docker-compose_base.yml.jinja",
            generated_file_path=docker_compose,
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="utils/config_interp.py.jinja",
            generated_file_path=src / "utils/config.py",
            jinja_env=jinja_env,
            render_args={},
        ),
    ]
    write_templates(template_file_structure)


def _run_redis_templates(config: Dict, jinja_env: Environment) -> None:
    """Runs templates related to Redis. All generated projects will use Redis as a cache regardless of selected techs.

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    :param jinja_env: The environment in which the Jinja should be executed
    :type jinja_env: Environment
    """
    src: Path = PathingManager().src
    test_dir: Path = PathingManager().tests
    docker_compose: Path = PathingManager().docker_compose
    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="connection/redis/redis_gen.py.jinja",
            generated_file_path=src / "connection/redis_connection.py",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="connection/redis/redis_test.py.jinja",
            generated_file_path=test_dir / "test_connection/test_redis_connection.py",
            jinja_env=jinja_env,
            render_args={},
        ),
    ]

    if not f"{config['project_name']}_cache:" in open(docker_compose, "r").read():
        template_file_structure.append(
            TemplateFileStructure(
                template_path="connection/redis/redis_docker_compose.yml.jinja",
                generated_file_path=docker_compose,
                jinja_env=jinja_env,
                render_args={"config": config},
            )
        )

    write_templates(template_file_structure)


def _run_pg_templates(config: Dict, jinja_env: Environment) -> None:
    """Runs templates related to postgres. Will only be executed if postgres is the selected database type

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    :param jinja_env: The environment in which the Jinja should be executed
    :type jinja_env: Environment
    """
    src: Path = PathingManager().src
    docker_compose: Path = PathingManager().docker_compose
    test_dir: Path = PathingManager().tests

    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="connection/postgres/pg_gen.py.jinja",
            generated_file_path=src / "connection/postgres_connection.py",
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="connection/postgres/pg_gen.py.jinja",
            generated_file_path=test_dir
            / "test_connection/test_postgres_connection.py",
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="logic/handlers/relational/generic_tools.py.jinja",
            generated_file_path=src / "logic/handlers/handler_utils/generic_tools.py",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="logic/handlers/relational/relational_crud_component.py.jinja",
            generated_file_path=src
            / "logic/handlers/handler_utils/crud_handler_component.py",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="logic/handlers/relational/relational_utils_component.py.jinja",
            generated_file_path=src
            / "logic/handlers/handler_utils/utils_handler_component.py",
            jinja_env=jinja_env,
            render_args={},
        ),
    ]

    if not f"{config['project_name']}_postgres:" in open(docker_compose, "r").read():
        template_file_structure.append(
            TemplateFileStructure(
                template_path="connection/postgres/pg_docker_compose.yml.jinja",
                generated_file_path=docker_compose,
                jinja_env=jinja_env,
                render_args={"config": config},
            )
        )

    for conversion in config["schematics"]:
        template_file_structure.append(
            TemplateFileStructure(
                template_path="model/pg_model.py.jinja",
                generated_file_path=src / f"models/{conversion.name.lower()}.py",
                jinja_env=jinja_env,
                render_args={"config": config, "schematic": conversion},
            )
        )
    template_file_structure.append(
        TemplateFileStructure(
            template_path="model/pg_association_tables.py.jinja",
            generated_file_path=src / "models/association_tables.py",
            jinja_env=jinja_env,
            render_args={"association_tables": config["association_tables"]},
        )
    )

    write_templates(template_file_structure)


def _run_grpc_templates(config: Dict, jinja_env: Environment) -> None:
    """Runs templates related to gRPC. Will only be executed if gRPC is the selected service type

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    :param jinja_env: The environment in which the Jinja should be executed
    :type jinja_env: Environment
    """

    src: Path = PathingManager().src
    docker_compose: Path = PathingManager().docker_compose
    root: Path = PathingManager().project_root
    dockerfile = PathingManager().dockerfile

    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="service/grpc/grpc_main_gen.py.jinja",
            generated_file_path=src / "main.py",
            jinja_env=jinja_env,
            render_args={"config": config, "schematics": config["schematics"]},
        ),
        TemplateFileStructure(
            template_path="protogen/protogen.sh.jinja",
            generated_file_path=root / "protogen.sh",
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="misc/grpc_dockerfile.jinja",
            generated_file_path=dockerfile,
            jinja_env=jinja_env,
            render_args={
                "config": config,
                "apt_dependencies": " ".join(get_apt_dependencies(config)),
            },
        ),
    ]

    if (
        not f"{config['project_name']}_grpc_service:"
        in open(docker_compose, "r").read()
    ):
        template_file_structure.append(
            TemplateFileStructure(
                template_path="service/grpc/grpc_docker_compose.yml.jinja",
                generated_file_path=docker_compose,
                jinja_env=jinja_env,
                render_args={"config": config},
            ),
        )

    for conversion in config["schematics"]:
        template_file_structure.append(
            TemplateFileStructure(
                template_path="logic/handlers/grpc/grpc_handler.py.jinja",
                generated_file_path=src
                / f"logic/handlers/{conversion.name.lower()}_handler.py",
                jinja_env=jinja_env,
                render_args={"config": config, "schematic": conversion},
            )
        )
        template_file_structure.append(
            TemplateFileStructure(
                template_path="service/grpc/grpc_routes_gen.py.jinja",
                generated_file_path=src
                / f"service/routes/{conversion.name.lower()}_routes.py",
                jinja_env=jinja_env,
                render_args={"config": config, "schematic": conversion},
            )
        )
        template_file_structure.append(
            TemplateFileStructure(
                template_path="protogen/proto_file_gen.proto.jinja",
                generated_file_path=root / f"proto/{conversion.name.lower()}.proto",
                jinja_env=jinja_env,
                render_args={
                    "config": config,
                    "schematic": conversion,
                    "non_default_variables": list(
                        conversion.grpc_variables | where(lambda x: x.default == False)
                    ),
                },
            )
        )

    write_templates(template_file_structure)


def _set_crud_instructions(config: Dict) -> None:
    """Sets the crud instructions to be applied. This is relevant because not all database paradigms support all CRUD instructions. E.g. delete isn't well supported with Cassandra.

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """
    database: str = config["database"]
    config["crud_instructions"] = []

    # Match hasn't been added in earlier Python versions
    if database == "Postgres":
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


def run_protogen(config: Dict) -> None:
    """Runs some subprocesses which uses the generated protogen file.
    This will only be executed if gRPC is the selected service type.
    The main point of the protogen file is to loop through all generated .proto file
    and generate the resulting .py files from the grpc python library.

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """
    relative_project_path = f"services/{config['project_name']}"
    protogen_sh = config["settings"]["file_structure"]["project_files"]["protogen_file"]

    subprocess.run(
        ["chmod", "+x", protogen_sh], check=True, text=True, cwd=relative_project_path
    )
    subprocess.run(["./protogen.sh"], check=True, text=True, cwd=relative_project_path)


def collect_dependencies(config: Dict) -> None:
    """Collects all Python dependencies to be used with poetry later on.
    These dependencies are stored within the config file, and will be appended according to the service and database types
    as well as some base dependencies and redis dependencies.

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """
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

    if service.lower() == "rest":
        dependencies = (
            dependencies + config["settings"]["server"]["rest"]["dependencies"]
        )
    elif service.lower() == "grpc":
        dependencies = (
            dependencies + config["settings"]["server"]["grpc"]["dependencies"]
        )
    elif service.lower() == "kafka":
        dependencies = (
            dependencies + config["settings"]["server"]["kafka"]["dependencies"]
        )
    elif service.lower() == "rabbitmq":
        dependencies = (
            dependencies + config["settings"]["server"]["rabbitmq"]["dependencies"]
        )
    else:
        print("Chosen service wasn't found. This should never happen")

    dependencies = (
        dependencies
        + config["settings"]["general_dependencies"]
        + config["settings"]["database"]["redis"]["dependencies"]
    )
    config["collected_dependencies"] = dependencies


def get_apt_dependencies(config: Dict) -> str:
    """Collects apt dependencies to be used in the generated Dockerfile. An example would be gcc with postgres

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    :return: Concatenation of all apt dependencies as a string.
    :rtype: str
    """
    database_settings: Dict = config["settings"]["database"]
    server_settings: Dict = config["settings"]["server"]

    return (
        database_settings.get(config["database"].lower())["debian_dependencies"]
        + server_settings.get(config["service"].lower())["debian_dependencies"]
    )


def _run_rest_templates(config: Dict, jinja_env: Environment):
    src: Path = PathingManager().src
    docker_compose: Path = PathingManager().docker_compose

    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="service/rest/rest_main_gen.py.jinja",
            generated_file_path=src / "main.py",
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
    ]

    if not f"{config['project_name']}_rest_service" in open(docker_compose, "r").read():
        template_file_structure.append(
            TemplateFileStructure(
                template_path="service/rest/rest_docker_compose.yml.jinja",
                generated_file_path=docker_compose,
                jinja_env=jinja_env,
                render_args={"config": config},
            )
        )
    for conversion in config["schematics"]:
        template_file_structure.append(
            TemplateFileStructure(
                template_path="service/rest/rest_routes_gen.py.jinja",
                generated_file_path=src
                / f"service/routes/{conversion.name.lower()}_routes.py",
                jinja_env=jinja_env,
                render_args={"config": config, "schematic": conversion},
            )
        )
        template_file_structure.append(
            TemplateFileStructure(
                template_path="logic/handlers/rest/rest_handler.py.jinja",
                generated_file_path=src
                / f"logic/handlers/{conversion.name.lower()}_handler.py",
                jinja_env=jinja_env,
                render_args={"config": config, "schematic": conversion},
            )
        )
    write_templates(template_file_structure)
