import os
import toml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
for _ in range(4):
    ROOT_DIR = ROOT_DIR = os.path.dirname(ROOT_DIR)
    
CONFIG_FILE_PATH = ROOT_DIR + "/config.toml"

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
print(f"Running on: {CONFIG['grpc']['host']}:{CONFIG['grpc']['port']}")