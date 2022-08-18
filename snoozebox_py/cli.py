from pathlib import Path
import sys
from typing import Dict, List
import os
import click
from utils.custom_errors import EmptySchematicsError
from utils.pathing import (
    create_directories_if_not_exists,
    create_empty_files_if_not_exists,
    get_directories_with_sql_files,
)

from snoozefile.snoozefile import generate_snoozefile
from gen.prompt import run_append_prompt
from snoozelib import sql_tables_to_classes
from snoozelib.conversion import Conversion
from gen.templates_management import templating_generation


@click.group()
def manager():
    pass


@manager.command()
@click.option(
    "--data-path",
    help="Configures the snoozefile to point to an already existing directory containing data",
)
def init():
    """Generates some basic files and directories to be used for appending services.
    """    
    create_directories_if_not_exists([Path("schematics"), Path("services")])
    create_empty_files_if_not_exists([Path("snoozefile.toml"), Path("docker-compose.yml")])
    generate_snoozefile()

        
@manager.command()
def append():
    """Runs the append prompt. Required for generating services.
    """    
    config: Dict = run_append_prompt()
    templating_generation(config=config)


@manager.command()
@click.option("--path", "-p")
@click.option("--translate", "-t", is_flag=True, help="Gives the snoozelib output")
def describe_sql(path, translate):
    """A CLI command for retrieving some information about the data inside the schematics directory. Contains flag for the snoozelib output

    :param path: Specific path to the schematics directory
    :type path: str
    :param translate: Flag for displaying information from the snoozelib library
    :type translate: boolean
    :raises EmptySchematicsError: error which gets raised if the directory is empty
    """
    if not path:
        path = os.getcwd()
    if not Path(path).is_dir():
        sys.exit("Path is not a directory. Please point to the schematics directory.")
    directories = get_directories_with_sql_files(Path(path))
    if not directories:
        raise EmptySchematicsError("No schematics with sql files")
    if translate:
        for file_lists in directories.values():
            for file_ in file_lists:
                conversions: List[Conversion] = []
                with open(file_, "r") as file_reader:
                    conversions = sql_tables_to_classes([file_reader.read()])
                    print(conversions)
                for conversion in conversions:
                    print(conversion.contents)
