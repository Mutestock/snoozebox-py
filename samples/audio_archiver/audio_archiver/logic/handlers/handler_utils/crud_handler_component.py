from sqlalchemy import insert, delete, update, select, inspect
from connection.pg_connection import exec_stmt
from typing import Any
from logic.handlers.handler_utils.generic_tools import prepare_object_for_querying

# https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html


class CrudHandlerComponent:
    def __init__(self, object_instance):
        self.table = object_instance.__table__

    def create(self, obj: object) -> None:
        exec_stmt(insert(self.table).values(prepare_object_for_querying(obj)))

    def read(self, id: int) -> Any:
        return exec_stmt(select(self.table).where(self.table.c.id == id)).fetchone()

    def update(self, id: int, obj: object) -> None:
        exec_stmt(
            update(self.table)
            .where(self.table.c.id == id)
            .values(prepare_object_for_querying(obj))
        )

    def delete(self, id: int) -> None:
        exec_stmt(delete(self.table).where(self.table.c.id == id))

    def read_list(self) -> list[Any]:
        return exec_stmt(select(self.table)).fetchall()
