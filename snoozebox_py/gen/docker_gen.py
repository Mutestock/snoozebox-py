import textwrap


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
    """)
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
