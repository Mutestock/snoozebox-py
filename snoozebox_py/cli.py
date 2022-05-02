import click


@click.group()
def manager():
    pass


@manager.command()
@click.option("--data-path",  help="Configures the snoozefile to point to an already existing directory containing data")
def init():
    pass


@manager.command()
def generate():
    pass
