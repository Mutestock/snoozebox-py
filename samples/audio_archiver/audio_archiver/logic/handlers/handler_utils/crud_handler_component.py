import json
from sqlalchemy import insert, delete, update, select
from connection.pg_connection import exec_stmt
from logic.handlers.handler_utils.generic_tools import (
    prepare_object_for_querying,
    iter_parse_datetime,
)
from connection.redis_connection import (
    redis_get,
    redis_set,
    redis_delete,
)
import logging
from pipe import map

# https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html


class CrudHandlerComponent:
    def __init__(self, object_instance) -> None:
        self.table = object_instance.__table__

    def create(self, obj: object) -> None:
        exec_stmt(insert(self.table).values(prepare_object_for_querying(obj)))
        self._clear_read_list_cache()

    def read(self, id: int) -> dict:
        cache_key: str = self._get_cache_key(id)

        cache_val = redis_get(cache_key)
        if cache_val:
            return json.loads(str(cache_val))
        else:
            res = (
                exec_stmt(select(self.table).where(self.table.c.id == id))
                .mappings()
                .first()
            )

            if res:
                res = iter_parse_datetime(res)
                redis_set(cache_key, json.dumps(res))
            return res

    def update(self, id: int, obj: object) -> None:
        cache_key: str = self._get_cache_key(id)

        exec_stmt(
            update(self.table)
            .where(self.table.c.id == id)
            .values(prepare_object_for_querying(obj))
        )
        
        redis_delete(cache_key)
        self._clear_read_list_cache()

    def delete(self, id: int) -> None:
        cache_key: str = self._get_cache_key(id)

        exec_stmt(delete(self.table).where(self.table.c.id == id))
        if redis_delete(cache_key) != 0:
            logging.info(f"Redis: {self.table} - id: {id} deleted")
        self._clear_read_list_cache()

    def read_list(self) -> list[dict]:
        cache_key: str = f"{self.table}-list"

        cache_val = redis_get(cache_key)
        if cache_val:
            return json.loads(str(cache_val))
        else:
            res = exec_stmt(select(self.table)).fetchall()
            if res:
                res = list(res | map(lambda x: iter_parse_datetime(x)))
                redis_set(cache_key, json.dumps(res))
        return res

    def _clear_read_list_cache(self) -> None:
        # Changes to the values of the database must invalidate the list
        cache_key: str = f"{self.table}-list"
        redis_delete(cache_key)

    def _get_cache_key(self, id) -> str:
        return f"{self.table}-{id}"
