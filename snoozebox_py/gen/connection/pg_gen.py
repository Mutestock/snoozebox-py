from gen.couple_writer_abstract import CoupleWriter
import textwrap

class PostgresConnection(CoupleWriter):
    subject: str = "connection"
    
    def write(self, config: dict):
        file_writer = open(
            f"{config.get('connection_path')}/postgres_connection.py", "w"
        )
        
        file_writer.writer(
            textwrap.dedent(
                """\
                    from sqlalchemy import create_engine
                    from sqlalchemy.ext.declarative import declarative_base
                    from utils.config import CONFIG
                    from typing import Optional, Any
                    
                    PG_CONFIG = CONFIG["database"]["postgres"]
                    
                    
                    conn_string = f'postgresql+psycopg2://{PG_CONFIG["usr"]}:{PG_CONFIG["pwd"]}@{PG_CONFIG["host"]}:{PG_CONFIG["port"]}/{PG_CONFIG["db"]}'
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
                """
            )
        )
        
    
    def write_test(self, config: dict):
        file_writer = open(
            file_writer = open(
            f"{config.get('test_path')}/test_connection/test_postgres.py", "w"
        )
        )
        file_writer.write(
            textwrap.dedent(
                """
                from connection.postgres_connection import engine
                from sqlalchemy_utils import database_exists
                
                
                class TestPostgres(unittest.testcase):
                    def test_connection(self):
                        self.assertTrue(database_exists(engine.url))
                """
            )
        )