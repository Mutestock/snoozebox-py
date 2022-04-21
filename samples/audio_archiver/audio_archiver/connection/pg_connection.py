from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from utils.config import CONFIG
from typing import Optional, Any

PG_CONFIG = CONFIG["db"]["postgres"]

conn_string = f'postgresql+psycopg2://{PG_CONFIG["db_user"]}:{PG_CONFIG["db_pwd"]}@{PG_CONFIG["host"]}:{PG_CONFIG["port"]}/{PG_CONFIG["db_name"]}'
engine = create_engine(conn_string, pool_size=20, max_overflow=0)
Base = declarative_base()



def db_init() -> None:
    Base.metadata.create_all(bind=engine, checkfirst=True)
    
def db_drop() -> None:
    Base.metadata.drop_all(bind=engine, checkfirst=True)


def exec_stmt(stmt) -> Optional[Any]:
    with engine.connect() as conn:
        result = conn.execute(stmt)
        return result
