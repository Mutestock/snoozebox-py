from jinja2 import Environment


def templating_prompt(jinja_env: Environment, config: dict = None) -> dict:
    if not config:
        config: dict = {}
    print("This is just going to be a lot of placeholders for now")
    