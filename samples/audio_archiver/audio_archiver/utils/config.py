import os
import toml

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_ROOT_DIR)

ROOT_DIR = os.path.dirname(_ROOT_DIR)
TEMPLATES_DIR = ROOT_DIR + "/audio_archiver/service/frontend/templates"
CONFIG_FILE_PATH = ROOT_DIR + "/config.toml"
LOG_FILE_PATH = ROOT_DIR + "/logs"

CONFIG = {}

_filename = CONFIG_FILE_PATH
_content: str = ""

with open(_filename) as f:
    _content = f.read()

CONFIG = toml.loads(_content)


def get_config_with_mode() -> dict:
    # Add more modes here. E.g. production
    if os.getenv("AUDIO_ARCHIVER_TESTING"):
        print("EXECUTION MODE IS: test")
        return CONFIG["test"]

    print("EXECUTION MODE IS: local")
    return CONFIG["local"]


CONFIG = get_config_with_mode()
