from sqlalchemy import insert, delete, update, select, inspect
from connection.pg_connection import exec_stmt
from typing import Any
from logic.handlers.handler_utils.generic_tools import prepare_object_for_querying
from connection.redis_connection import get_cache_value, set_cache_value

# https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html


class CrudHandlerComponent:
    def __init__(self, object_instance):
        self.table = object_instance.__table__

    def create(self, obj: object) -> None:
        exec_stmt(insert(self.table).values(prepare_object_for_querying(obj)))

    def read(self, id: int) -> Any:
        cache_key: str = f"{self.table}-{id}"
        
        cache_val = get_cache_value(cache_key)
        if cache_val:
            return str(cache_val)
        else:
            res = exec_stmt(select(self.table).where(self.table.c.id == id)).first()
            print(f"REEEEEEEEEEEES: {res}")
            if res:
                set_cache_value(cache_key, str(res))
        return res

    def update(self, id: int, obj: object) -> None:
        exec_stmt (
            update(self.table)
            .where(self.table.c.id == id)
            .values(prepare_object_for_querying(obj))
        )

    def delete(self, id: int) -> None:
        exec_stmt(delete(self.table).where(self.table.c.id == id))

    def read_list(self) -> list[Any]:
        cache_key: str = f"{self.table}-list"
        
        cache_val = get_cache_value(cache_key)
        if cache_val:
            return cache_val
        else:
            res = exec_stmt(select(self.table)).fetchall()
            if res:
                set_cache_value(cache_key, str(res))
        return res
