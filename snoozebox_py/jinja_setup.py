from jinja2 import Environment, Packageloader, select_autoescape

def setup_templating() -> Environment:
    return Environment(
        loader=Packageloader("gen"),
        autoescape=select_autoescape
    )