from gen.couple_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_directory, get_relative_tests_directory
import textwrap


class PostgresConnection(BlockWriter):
    subject: str = "connection"

    def write(self, config: dict):
        file_writer = open(
            f"{get_relative_project_directory(config)}/{config['settings']['file_structure']['connection']}/postgres_connection.py",
            "w",
        )

        file_writer.write(
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
            f"{get_relative_tests_directory()}/test_connection/test_postgres.py", "w"
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
