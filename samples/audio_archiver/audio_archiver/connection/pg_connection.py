from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from utils.config import CONFIG

PG_CONFIG = CONFIG["db"]["pg"]

conn_string = f'postgresql+psycopg2://{PG_CONFIG["db_user"]}:{PG_CONFIG["db_pwd"]}@{PG_CONFIG["host"]}:{PG_CONFIG["port"]}/{PG_CONFIG["db_name"]}'
engine = create_engine(conn_string, pool_size=20, max_overflow=0)
Base = declarative_base()


def db_init():
    Base.metadata.create_all(engine)

def exec_stmt(stmt):
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
        return result
    