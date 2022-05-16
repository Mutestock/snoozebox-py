from typing import List
import click
from utils.pathing import (
    create_directories_if_not_exists,
    create_empty_files_if_not_exists,
)

from snoozefile.snoozefile import generate_snoozefile
from gen.prompt import run_append_prompt
from gen.gen_base import exec_gen
from snoozelib import sql_tables_to_classes
from snoozelib.conversion import Conversion


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


@manager.command()
@click.option("--path","-p", required=True, help="Point to the sql file to translate")
def translate(path):
    conversions: List[Conversion] = []
    with open(path, "r") as file_reader:
        conversions = sql_tables_to_classes(file_reader.read())
        print(conversions)
    for conversion in conversions:
        print(conversion.contents)