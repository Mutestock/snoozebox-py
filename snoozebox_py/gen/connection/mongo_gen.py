from gen.couple_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_directory
import textwrap


class MongoConnection(BlockWriter):
    subject: str = "connection"

    def write(self, config: dict) -> None:
        file_writer = open(f"{get_relative_project_directory(config)}/{config['settings']['file_structure']['connection']}//mongo_connection.py")

        file_writer.write(
            textwrap.dedent(
                f"""\
                from pymongo import MongoClient
                from utils.config import CONFIG
                
                MONGO_CONFIG = CONFIG["database"]["mongo"]
                
                client = MongoClient(
                    host=CONFIG["host"],
                    port=MONGO_CONFIG["port"], 
                    username=MONGO_CONFIG["usr"],
                    password=MONGO_CONFIG["pwd"],
                )
                """
            )
        )
        file_writer.close()

    def write_test(self, config: dict) -> None:
        file_writer = open(
            f"{config.get('test_path')}/test_connection/test_mongo.py", "w"
        )
        
        file_writer.write(
            textwrap.dedent(
                f"""\
                import unittest
                
                from connection.mongo_connection import client
                
                class TestMongo(unittest.testcase):
                    def test_mongo_connection(self):
                        self.assertTrue(client.server_info()!=None)
                """
            )
        )
        
        
