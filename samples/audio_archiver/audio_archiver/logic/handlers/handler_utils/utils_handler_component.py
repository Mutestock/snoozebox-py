from sqlalchemy import select, inspect
from sqlalchemy import func


class UtilsHandlerComponent:
    def __init__(self, object_instance):
        self.table = object_instance.__table__


    def count(self):
        return select([func.count()]).select_from(self.table).scalar()
