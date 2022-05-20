from gen.block_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_root_directory, get_relative_tests_directory
import textwrap

class RedisConnection(BlockWriter):
    subject: str = "connection"
    
    def write(self, config: dict) -> None:
        
        project_directories: dict = config['settings']['file_structure']['project_directories']
        connection: str = project_directories['connection'][0]
        utils: str = project_directories['utils'][0]
        
        file_writer = open(
            f"{get_relative_project_root_directory(config)}/{connection}/redis_connection.py", "w"
        )
        
        file_writer.write(
            textwrap.dedent(f"""\
            from redis import StrictRedis
            from {utils}.config import CONFIG
            from typing import Optional, Any

            REDIS_CONFIG: dict = CONFIG["db"]["redis"]


            def get_cache_pool(settings: dict = None) -> StrictRedis:
                if not settings: settings = REDIS_CONFIG

                return StrictRedis(
                    host=settings["host"],
                    port=settings["port"],
                    password=settings["pwd"],
                    charset="utf-8",
                    db=settings["db"],
                    decode_responses=True,
                )


            def redis_exists(key: str) -> bool:
                return get_cache_pool().exists(key) == 1


            def redis_get(key: str) -> Optional[Any]:
                return get_cache_pool().get(key)


            def redis_set(key: str, value: str) -> Optional[bool]:
                return get_cache_pool().set(key, value)


            def redis_hset(key: str, value: dict) -> Optional[int]:
                return get_cache_pool().hset(key, mapping=value)


            def redis_delete(key: str) -> Optional[int]:
                return get_cache_pool().delete(key)


            def redis_flush():
                return get_cache_pool().flushdb()
            """
            )
        )

    
    
    def write_test(self, config: dict) -> None:
        
        connection: str = config['settings']['file_structure']['project_directories']['connection'][0]
        
        file_writer = open(
            f"{get_relative_tests_directory(config)}/{config['settings']['file_structure']['test_directories']['test_connection'][0]}/test_cassandra.py", "w"
        )

        file_writer.write(
            textwrap.dedent(
                f"""\
            import unittest
            from {connection}.redis_connection import get_cache_pool
            
            
            class TestRedis(unittest.testcase):
                def test_connection(self):
                    redis_set("test_key", "test_value")
                    self.assertTrue(str(redis_get("test_key")), "test_value")
            
            """
            )
        )
        file_writer.close()