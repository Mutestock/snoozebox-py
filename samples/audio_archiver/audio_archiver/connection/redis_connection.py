from redis import Redis
from utils.config import CONFIG

REDIS_CONFIG = CONFIG["db"]["redis"]


def get_cache_pool() -> Redis:
    return Redis(
        host=REDIS_CONFIG["host"],
        port=REDIS_CONFIG["port"],
        password=REDIS_CONFIG["pwd"],
    )

def get_cache_value(key: str) -> str:
    return get_cache_pool().get(key)

def set_cache_value(key: str, value: str) -> bool:
    return get_cache_pool().set(key, value)
    