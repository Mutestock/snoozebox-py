from gen.block_writer_abstract import BlockWriter
from utils.pathing import (
    get_relative_project_src_directory,
    get_relative_tests_directory,
    get_relative_generated_config_file,
)
import textwrap


class PostgresConnection(BlockWriter):
    subject: str = "connection"

    def write(self, config: dict):
        
        project_directories: dict = config['settings']['file_structure']['project_directories']
        connection: str = project_directories['connection'][0]
        utils: str = project_directories['utils'][0]
        
        file_writer = open(
            f"{get_relative_project_src_directory(config)}/{connection}/postgres_connection.py",
            "w",
        )

        file_writer.write(
            textwrap.dedent(
                f"""\
                    from sqlalchemy import create_engine
                    from sqlalchemy.ext.declarative import declarative_base
                    from {utils}.config import CONFIG
                    from typing import Optional, Any
                    
                    PG_CONFIG = CONFIG["database"]["postgres"]
                    
                    
                    conn_string = f'postgresql+psycopg2://{{PG_CONFIG["usr"]}}:{{PG_CONFIG["pwd"]}}@{{PG_CONFIG["host"]}}:{{PG_CONFIG["port"]}}/{{PG_CONFIG["db"]}}'
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
        
        connection: str = config['settings']['file_structure']['project_directories']['connection'][0]
        
        file_writer = open(
            f"{get_relative_tests_directory(config)}/{config['settings']['file_structure']['test_directories']['test_connection'][0]}/test_postgres.py",
            "w",
        )

        file_writer.write(
            textwrap.dedent(
                f"""
                from {connection}.postgres_connection import engine
                from sqlalchemy_utils import database_exists
                
                
                class TestPostgres(unittest.testcase):
                    def test_connection(self):
                        self.assertTrue(database_exists(engine.url))
                """
            )
        )

    def docker_compose_write(self, config: dict) -> None:
        file_writer = open(config["settings"]["file_structure"]["docker_compose"])

    def config_write(self, config: dict) -> None:
        file_writer = open(get_relative_generated_config_file(config))
