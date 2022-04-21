from redis import StrictRedis
from utils.config import CONFIG
from typing import Optional, Any

REDIS_CONFIG = CONFIG["db"]["redis"]


def get_cache_pool() -> StrictRedis:
    return StrictRedis(
        host=REDIS_CONFIG["host"],
        port=REDIS_CONFIG["port"],
        password=REDIS_CONFIG["pwd"],
        charset="utf-8",
        decode_responses=True
    )

def redis_exists(key: str) -> bool:
    return get_cache_pool().exists(key)==1


def get_cache_value(key: str) -> Optional[Any]:
    return get_cache_pool().get(key)


def set_cache_value(key: str, value: str) -> Optional[bool]:
    return get_cache_pool().set(key, value)
