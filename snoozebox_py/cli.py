from pathlib import Path
import sys
from typing import List
import os
import click
from utils.pathing import (
    create_directories_if_not_exists,
    create_empty_files_if_not_exists,
    get_directories_with_sql_files,
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
@click.option("--path", "-p", required=True, help="Point to the sql file to translate")
def translate(path):
    conversions: List[Conversion] = []
    with open(path, "r") as file_reader:
        conversions = sql_tables_to_classes(file_reader.read())
        print(conversions)
    for conversion in conversions:
        print(conversion.contents)


@manager.command()
@click.option("--path", "-p")
@click.option("--translate", "-t", is_flag=True, help="Gives the snoozelib output")
def describe_sql(path, translate):
    """
    Returns a dictionary with basic information about the found sql files in the directory structure
    Point to the schematics folder with path variable or execute this command inside the schematics folder

    """
    if not path:
        path = os.getcwd()
    if not Path(path).is_dir():
        sys.exit("Path is not a directory. Please point to the schematics directory.")
    directories = get_directories_with_sql_files(path)
    print(directories)
    if translate:
        for file_lists in directories.values():
            for file_ in file_lists:
                conversions: List[Conversion] = []
                with open(file_, "r") as file_reader:
                    conversions = sql_tables_to_classes(file_reader.read())
                    print(conversions)
                for conversion in conversions:
                    print(conversion.contents)
