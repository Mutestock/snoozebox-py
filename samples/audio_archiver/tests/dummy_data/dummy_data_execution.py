from sqlalchemy import text
from sqlalchemy.engine import Engine

DUMMY_DATA_DIRECTORY: str = "tests/dummy_data"
AVAILABLE_DUMMY_DATA: dict = {
    "channel": f"{DUMMY_DATA_DIRECTORY}/channel_dummy_data.sql",
    "audio": f"{DUMMY_DATA_DIRECTORY}/audio_dummy_data.sql"
}


def create_dummy_data(engine: Engine, dummy_data_type: str) -> None:
    with engine.connect() as conn:
        with open(str(AVAILABLE_DUMMY_DATA.get(dummy_data_type))) as file:
            query = text(file.read())
            conn.execute(query)
    