from gen.couple_writer_abstract import CoupleWriter
import textwrap

class RedisConnection(CoupleWriter):
    subject: str = "connection"
    
    def write(self, config: dict) -> None:
        file_writer = open(
            f"{config.get('connection_path')}/redis_connection.py", "w"
        )
        
        file_writer.write(
            textwrap.dedent("""\
            from redis import StrictRedis
            from utils.config import CONFIG
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
        file_writer = open(
            f"{config.get('test_path')}/test_connection/test_cassandra.py", "w"
        )

        file_writer.write(
            textwrap.dedent(
                f"""\
            import unittest
            from connection.redis_connection import get_cache_pool
            
            
            class TestRedis(unittest.testcase):
                def test_connection(self):
                    redis_set("test_key", "test_value")
                    self.assertTrue(str(redis_get("test_key")), "test_value")
            
            """
            )
        )
        file_writer.close()