import textwrap
from utils.pathing import get_relative_project_root_directory, indent_writer


DOCKER_COMPOSE_PREFIX_CONTENTS = textwrap.dedent(
    """\
    version: "3"
    
    services:
    """
)


def initial_docker_compose_check(config: dict):
    if not _docker_compose_contains_content(config, DOCKER_COMPOSE_PREFIX_CONTENTS):
        _docker_compose_append_content(config, DOCKER_COMPOSE_PREFIX_CONTENTS)


def final_docker_compose_check(config: dict):
    content = textwrap.dedent(
        f"""\
        networks:
          {config["settings"]["docker_compose_network"]}:
            driver: "bridge"
    """
    )
    if not _docker_compose_contains_content(config, content):
        _docker_compose_append_content(config, content)


def _docker_compose_contains_content(config: dict, content: str) -> bool:
    file_reader = open(config["settings"]["file_structure"]["docker_compose"], "r")
    contains_contents: bool = content in file_reader.read()
    file_reader.close()
    return contains_contents


def _docker_compose_append_content(config: dict, content: str) -> None:
    file_writer = open(config["settings"]["file_structure"]["docker_compose"], "a")
    file_writer.write(content)
    file_writer.close()


def _get_apt_dependencies(config: dict) -> str:
    database_settings: dict = config["settings"]["database"]
    server_settings: dict = config["settings"]["server"]

    return (
        database_settings.get(config["database"].lower())["debian_dependencies"]
        + server_settings.get(config["service"].lower())["debian_dependencies"]
    )


def write_docker_file(config: dict) -> None:
    {
        "rest": rest_dockerfile,
        "grpc": grpc_dockerfile,
        "kafka": kafka_dockerfile,
        "rabbitmq": rabbitmq_dockerfile,
    }.get(config["service"].lower())(config)


def grpc_dockerfile(config: dict) -> None:
    file_writer = open(get_relative_project_root_directory(config) + "/Dockerfile", "w")
    indent_writer(
        lvl=0,
        text=f"""
            FROM python:3.9-slim
            COPY . /app
            WORKDIR /app
            RUN apt-get update
            RUN apt-get install {" ".join(_get_apt_dependencies(config))}
            RUN pip install -r requirements.txt
            CMD ["python", "audio_archiver/main.py"]
    """,
        file_writer=file_writer,
    )
    file_writer.close()


def rest_dockerfile(config: dict) -> None:
    pass


def kafka_dockerfile(config: dict) -> None:
    pass


def rabbitmq_dockerfile(config: dict) -> None:
    pass
