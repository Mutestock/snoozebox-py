import os
import toml

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_ROOT_DIR)

ROOT_DIR = os.path.dirname(_ROOT_DIR)
# CONFIG_FILE_PATH = ROOT_DIR + "/config.toml"
LOG_FILE_PATH = ROOT_DIR + "/logs"
DOCKER_COMPOSE_STRINGS_PATH = ROOT_DIR + "/docker-compose-strings.toml"
DEFAULT_SETTINGS_PATH = ROOT_DIR + "/default_settings.toml"

CONFIG: dict = {}


for toml_file in [DOCKER_COMPOSE_STRINGS_PATH, DEFAULT_SETTINGS_PATH]:
    with open(toml_file, "r") as file_reader:
        content = file_reader.read()
        if content:
            CONFIG.update(toml.loads(content))
        
