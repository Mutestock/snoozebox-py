from dataclasses import dataclass
from io import TextIOWrapper
from typing import List
from jinja2 import Environment, PackageLoader, select_autoescape
from gen.gen_base import _collect_dependencies
from .config_gen import write_config
from .docker_gen import get_apt_dependencies
from utils.poetry_exec import run_poetry, poetry_export_requirements
from utils.pathing import (
    create_mode_specific_directories,
    get_relative_project_root_directory,
    get_relative_project_src_directory,
    get_relative_tests_directory,
    get_docker_compose_file,
    create_base_directories,
)
from gen.gitignore_gen import write_git_ignore
from pipe import where
from gen.protogen import run_protogen
import subprocess

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
    create_mode_specific_directories(config)
    _set_crud_instructions(config)
    _run_base_templates(config, jinja_env)
    _run_redis_templates(config, jinja_env)
    _determine_and_run_service_templates(config, jinja_env)
    _determine_and_run_database_templates(config, jinja_env)
    write_git_ignore(config)
    write_config(config)
    run_protogen(config)
    print("Done")


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
    src: str = get_relative_project_src_directory(config)
    docker_compose: str = get_docker_compose_file(config)
    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="misc/docker-compose_base.yml.jinja",
            generated_file_path=docker_compose,
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="utils/config_interp.py.jinja",
            generated_file_path=f"{src}/utils/config.py",
            jinja_env=jinja_env,
            render_args={},
        ),
    ]
    _write_templates(template_file_structure)


def _run_redis_templates(config: dict, jinja_env: Environment) -> None:
    src: str = get_relative_project_src_directory(config)
    test_dir: str = get_relative_tests_directory(config)
    docker_compose: str = get_docker_compose_file(config)
    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="connection/redis/redis_gen.py.jinja",
            generated_file_path=f"{src}/connection/redis_connection.py",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="connection/redis/redis_test.py.jinja",
            generated_file_path=f"{test_dir}/test_connection/test_redis_connection.py",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="connection/redis/redis_docker_compose.yml.jinja",
            generated_file_path=docker_compose,
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
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
            generated_file_path=f"{src}/logic/handlers/handler_utils/generic_tools.py",
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
    _write_templates(template_file_structure)


def _run_grpc_templates(config: dict, jinja_env: Environment) -> None:
    src: str = get_relative_project_src_directory(config)
    docker_compose: str = get_docker_compose_file(config)
    root: str = get_relative_project_root_directory(config)
    dockerfile = f"{root}/Dockerfile"
    

    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="service/grpc/grpc_docker_compose.yml.jinja",
            generated_file_path=docker_compose,
            jinja_env=jinja_env,
            render_args={"config": config},
        ),
        TemplateFileStructure(
            template_path="service/grpc/grpc_main_gen.py.jinja",
            generated_file_path=f"{src}/main.py",
            jinja_env=jinja_env,
            render_args={"config": config, "schematics": config["schematics"]},
        ),
        TemplateFileStructure(
            template_path="protogen/protogen.sh.jinja",
            generated_file_path=f"{root}/protogen.sh",
            jinja_env=jinja_env,
            render_args={"config": config}
        ),
        TemplateFileStructure(
            template_path="misc/grpc_dockerfile.jinja",
            generated_file_path=dockerfile,
            jinja_env=jinja_env,
            render_args={"config": config, "apt_dependencies": " ".join(get_apt_dependencies(config))}       
        )
    ]
    for schematic in config["schematics"]:
        for conversion in schematic:
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
            template_file_structure.append(
                TemplateFileStructure(
                    template_path="protogen/proto_file_gen.proto.jinja",
                    generated_file_path=f"{root}/proto/{conversion.name.lower()}.proto",
                    jinja_env=jinja_env,
                    render_args={
                        "config": config,
                        "schematic": conversion,
                        "non_default_variables": list(
                            conversion.grpc_variables
                            | where(lambda x: x.default == False)
                        ),
                    },
                )
            )

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


def run_protogen(config: dict) -> None:
    relative_project_path = f"services/{config['project_name']}"
    protogen_sh = config["settings"]["file_structure"]["project_files"]["protogen_file"]

    subprocess.run(
        ["chmod", "+x", protogen_sh], check=True, text=True, cwd=relative_project_path
    )
    subprocess.run(["./protogen.sh"], check=True, text=True, cwd=relative_project_path)