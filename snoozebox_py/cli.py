import click
from utils.pathing import (
    create_directories_if_not_exists,
    create_empty_files_if_not_exists,
)

from snoozefile.snoozefile import generate_snoozefile
from gen.prompt import run_append_prompt
from gen.gen_base import exec_gen


@click.group()
def manager():
    pass


@manager.command()
@click.option(
    "--data-path",
    help="Configures the snoozefile to point to an already existing directory containing data",
)
def init(data_path):
    create_directories_if_not_exists(["schematics", "services"])
    create_empty_files_if_not_exists(["snoozefile.toml", "docker-compose.yml"])
    generate_snoozefile()


@manager.command()
def generate():
    pass


@manager.command()
def append():
    config: dict = run_append_prompt()
    exec_gen(config)
