
from sqlalchemy import insert, delete, update, select, inspect
from connection.pg_connection import exec_stmt

# https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html


class CrudHandlerComponent:
    def __init__(self, object_instance):
        self.table = object_instance.__table__

    def create(self, obj: object):
        exec_stmt(insert(self.table).values(obj))

    def read(self, id: int):
        return exec_stmt(select(self.table).where(self.table.c.id == id))

    def update(self, id: int, obj: object):
        exec_stmt(update(self.table).where(self.table.c.id == id).values(obj))

    def delete(self, id: int):
        exec_stmt(delete(self.table).where(self.table.c.id == id))

    def read_list(self) -> list:
        return exec_stmt(select(self.table))
