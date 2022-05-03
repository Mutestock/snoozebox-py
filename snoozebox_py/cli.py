import click
import os


@click.group()
def manager():
    pass


@manager.command()
@click.option("--data-path",  help="Configures the snoozefile to point to an already existing directory containing data")
def init():
    if not os.path.exists("schematics"):
        os.mkdir("schematics")
    if not os.path.exists("snoozefile.toml"):
        open("snoozefile.toml","w").close()
    


@manager.command()
def generate():
    pass

@manager.command()
def append():
    pass



