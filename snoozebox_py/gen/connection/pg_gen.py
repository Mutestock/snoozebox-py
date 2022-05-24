from typing import List
from gen.block_writer_abstract import BlockWriter
from gen.config_gen import dict_recurse_define
from utils.pathing import (
    get_relative_project_src_directory,
    get_relative_tests_directory,
    get_relative_generated_config_file,
)
from utils.pathing import indent_writer
from pipe import select


class PostgresConnection(BlockWriter):
    subject: str = "connection"

    def write(self, config: dict):

        project_directories: dict = config["settings"]["file_structure"][
            "project_directories"
        ]
        connection: str = project_directories["connection"][0]
        utils: str = project_directories["utils"][0]

        file_writer = open(
            f"{get_relative_project_src_directory(config)}/{connection}/postgres_connection.py",
            "w",
        )

        indent_writer(
            lvl=0,
            text=f"""
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
                """,
            file_writer=file_writer,
        )
        file_writer.close()

    def write_test(self, config: dict):
        connection: str = config["settings"]["file_structure"]["project_directories"][
            "connection"
        ][0]

        file_writer = open(
            f"{get_relative_tests_directory(config)}/{config['settings']['file_structure']['test_directories']['test_connection'][0]}/test_postgres.py",
            "w",
        )

        indent_writer(
            lvl=0,
            text=f"""
                from {connection}.postgres_connection import engine
                from sqlalchemy_utils import database_exists
                
                
                class TestPostgres(unittest.testcase):
                    def test_connection(self):
                        self.assertTrue(database_exists(engine.url))
                """,
            file_writer=file_writer,
        )

        file_writer.close()

    def write_docker_compose(self, config: dict) -> None:
        file_writer = open(config["settings"]["file_structure"]["docker_compose"], "a")

        indent_writer(
            lvl=2,
            text=f"""
            {config['project_name']}_postgres:
                container_name: {config['project_name']}_postgres
                image: postgres:latest
                restart: always
                environment:
                  - POSTGRES_USER={config['settings']['database']['postgres']['usr']}
                  - POSTGRES_PASSWORD={config['settings']['database']['postgres']['pwd']}
                  - POSTGRES_DB={config['settings']['database']['postgres']['db']}
                  - PGDATA=/var/lib/postgresql/data
                ports:
                  - xcvpkfposdkfpsodkf:5432
                volumes:
                  - ./data/postgres:/var/lib/postgresql/data
                networks:
                  - {config["settings"]["docker_compose_network"]}
        """,
            file_writer=file_writer,
        ),

        indent_writer(
            lvl=2,
            text=f"""
            
            {config['project_name']}_test_postgres:
                container_name: {config['project_name']}_test_postgres
                image: postgres:latest
                restart: always
                environment:
                  - POSTGRES_USER={config['settings']['database']['postgres']['usr']}
                  - POSTGRES_PASSWORD={config['settings']['database']['postgres']['pwd']}
                  - POSTGRES_DB={config['settings']['database']['postgres']['db']}
                  - PGDATA=/var/lib/postgresql/data
                ports:
                  - xcvpkfposdkfpsodkf:5432
                volumes:
                  - ./data/postgres_test:/var/lib/postgresql/data
                networks:
                  - {config["settings"]["docker_compose_network"]}
        """,
            file_writer=file_writer,
        )

        file_writer.close()

    def write_config(self, config: dict) -> None:
        def mode_write(config: dict, mode: str) -> None:
            dict_recurse_define(
                config, ["relative_config_toml", mode, "database", "postgres"]
            )
            config["relative_config_toml"][mode]["database"]["postgres"][
                "host"
            ] = config["settings"]["database"]["postgres"]["host"]
            config["relative_config_toml"][mode]["database"]["postgres"][
                "port"
            ] = config["settings"]["database"]["postgres"]["port"]
            config["relative_config_toml"][mode]["database"]["postgres"][
                "usr"
            ] = config["settings"]["database"]["postgres"]["usr"]
            config["relative_config_toml"][mode]["database"]["postgres"][
                "pwd"
            ] = config["settings"]["database"]["postgres"]["pwd"]
            config["relative_config_toml"][mode]["database"]["postgres"]["db"] = config[
                "settings"
            ]["database"]["postgres"]["host"]

        list(["local", "test"] | select(lambda x: mode_write(config, x)))
