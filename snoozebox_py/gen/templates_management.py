from dataclasses import dataclass
from io import TextIOWrapper
from typing import List
from jinja2 import Environment, PackageLoader, select_autoescape
from gen.gen_base import _collect_dependencies
from utils.poetry_exec import run_poetry, poetry_export_requirements
from utils.pathing import (
    get_relative_project_src_directory,
    get_relative_tests_directory,
    get_docker_compose_file,
    create_base_directories,
)
from pprint import pprint


@dataclass
class TemplateFileStructure:
    template_path: str
    generated_file_path: str
    jinja_env: Environment
    render_args: dict

    def get_render(self) -> str:
        return self.jinja_env.get_template(self.template_path).render(self.render_args)


def _setup_templating() -> Environment:
    return Environment(loader=PackageLoader("gen"), autoescape=select_autoescape)


def templating_prompt(jinja_env: Environment = None, config: dict = None) -> dict:
    print("This is just going to be a lot of placeholders for now")

    if not config:
        config: dict = {}
    if not jinja_env:
        jinja_env: Environment = _setup_templating()

    _collect_dependencies(config)
    run_poetry(config)
    poetry_export_requirements(config)
    create_base_directories(config)
    _set_crud_instructions(config)
    _run_base_templates(config, jinja_env)
    _determine_and_run_service_templates(config, jinja_env)
    _determine_and_run_database_templates(config, jinja_env)


def _determine_and_run_service_templates(config: dict, jinja_env: Environment) -> None:
    {"rest": None, "grpc": _run_grpc_templates, "kafka": None, "rabbitmq": None,}.get(
        config["service"].lower()
    )(config, jinja_env)


def _determine_and_run_database_templates(config: dict, jinja_env: Environment) -> None:
    {"postgres": _run_pg_templates, "mongodb": None, "cassandra": None}.get(
        config["database"].lower()
    )(config, jinja_env)


def _write_templates(template_file_structure: List[TemplateFileStructure]) -> None:
    for template_file in template_file_structure:
        file_writer: TextIOWrapper = open(template_file.generated_file_path, "a")
        file_reader: TextIOWrapper = open(template_file.generated_file_path, "r")
        render: str = template_file.get_render()
        current: str = "".join(file_reader.readlines())

        # These two are just for comparing
        stripped_render: str = render.replace(" ", "").rstrip()
        stripped_current: str = current.replace(" ", "").rstrip()

        if not stripped_render in stripped_current:
            file_writer.write(render)


def _run_base_templates(config: dict, jinja_env: Environment) -> None:
    docker_compose: str = get_docker_compose_file(config)
    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="misc/docker-compose_base.yml.jinja",
            generated_file_path=docker_compose,
            jinja_env=jinja_env,
            render_args={"config": config},
        )
    ]
    _write_templates(template_file_structure)


def _run_pg_templates(config: dict, jinja_env: Environment) -> None:
    src: str = get_relative_project_src_directory(config)
    docker_compose: str = get_docker_compose_file(config)
    test_dir: str = get_relative_tests_directory(config)

    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="connection/postgres/pg_gen.py.jinja",
            generated_file_path=f"{src}/connection/postgres_connection.py",
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="connection/postgres/pg_gen.py.jinja",
            generated_file_path=f"{test_dir}/test_connection/test_postgres_connection.py",
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="connection/postgres/pg_docker_compose.yml.jinja",
            generated_file_path=docker_compose,
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="logic/handlers/relational/generic_tools.py.jinja",
            generated_file_path=f"{src}/logic/generic_tools.py",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="logic/handlers/relational/relational_crud_component.py.jinja",
            generated_file_path=f"{src}/logic/handlers/handler_utils/crud_handler_component.py",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="logic/handlers/relational/relational_utils_component.py.jinja",
            generated_file_path=f"{src}/logic/handlers/handler_utils/utils_handler_component.py",
            jinja_env=jinja_env,
            render_args={},
        ),
    ]
    for schematic in config["schematics"]:
        for conversion in schematic:
            template_file_structure.append(
                TemplateFileStructure(
                    template_path="model/pg_model.py.jinja",
                    generated_file_path=f"{src}/models/{conversion.name.lower()}.py",
                    jinja_env=jinja_env,
                    render_args={"config": config, "schematic": conversion},
                )
            )
            template_file_structure.append(
                TemplateFileStructure(
                    template_path="logic/handlers/grpc/grpc_handler.py.jinja",
                    generated_file_path=f"{src}/logic/handlers/{conversion.name.lower()}_handler.py",
                    jinja_env=jinja_env,
                    render_args={"config": config, "schematic": conversion},
                )
            ),
            template_file_structure.append(
                TemplateFileStructure(
                    template_path="service/grpc/grpc_routes_gen.py.jinja",
                    generated_file_path=f"{src}/service/routes/{conversion.name.lower()}_routes.py",
                    jinja_env=jinja_env,
                    render_args={"config": config, "schematic": conversion},
                )
            )
    _write_templates(template_file_structure)


def _run_grpc_templates(config: dict, jinja_env: Environment) -> None:
    src: str = get_relative_project_src_directory(config)
    docker_compose: str = get_docker_compose_file(config)
    test_dir: str = get_relative_tests_directory(config)

    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="service/grpc/grpc_docker_compose.yml.jinja",
            generated_file_path=docker_compose,
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="service/grpc/grpc_main_gen.py.jinja",
            generated_file_path=f"{src}/service/grpc_main.py",
            jinja_env=jinja_env,
            render_args={"config": config, "schematics": config["schematics"]},
        ),
    ]
    _write_templates(template_file_structure)


def _set_crud_instructions(config: dict) -> None:
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
