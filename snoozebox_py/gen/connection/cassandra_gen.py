from gen.couple_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_directory
import textwrap


class CassandraConnection(BlockWriter):
    subject: str = "connection"

    def write(self, config: dict) -> None:
        file_writer = open(
            f"{get_relative_project_directory(config)}/{config['settings']['file_structure']['connection']}/cassandra_connection.py", "w"
        )

        file_writer.write(
            textwrap.dedent(
                f"""\
            from cassandra.cluster import Cluster
            from cassandra.auth import PlainTextAuthProvider
            from utils.config import CONFIG
            
            CASSANDRA_CONFIG = CONFIG["database"]["cassandra"]
            
            auth_provider = PlainTextAuthProvider(
                username=CASSANDRA_CONFIG["usr"], 
                password=CASSANDRA_CONFIG["pwd],
            )
            
            cluster = Cluster(
                [CASSANDRA_CONFIG["host"]], 
                port=CASSANDRA_CONFIG["port"], 
                auth_provider=auth_provider
            )
            
            def get_cassandra_session(keyspace: str = NONE):
                if not keyspace:
                    keyspace = CASSANDRA_CONFIG["keyspace"]
                return cluster.connect(keyspace)
            """
            )
        )
        file_writer.close()

    def write_test(self, config: dict) -> None:
        file_writer = open(
            f"{config.get('test_path')}/test_connection/test_cassandra.py", "w"
        )

        file_writer.write(
            textwrap.dedent(
                f"""\
            import unittest
            from connection.cassandra_connection import get_cassandra_connection
            
            
            class TestCassandra(unittest.testcase):
                def test_connection(self):
                    stmt = session.prepare("SELECT now() FROM system.local;)
                    res = session.execute(stmt)
                    self.assertTrue(res!=None)
            
        """
            )
        )
        file_writer.close()
        
    def docker_compose_write(self, config: dict) -> None:
        pass
    
    def config_write(self, config: dict ) -> None:
        pass