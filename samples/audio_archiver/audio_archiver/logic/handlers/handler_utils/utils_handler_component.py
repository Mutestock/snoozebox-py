from sqlalchemy import select, inspect
from sqlalchemy import func

class UtilsHandlerComponent():
    
    def __init__(self, object_instance: object):
        self.table = inspect(object_instance).local_table
    
    def count(self):
        return select([func.count()]).select_from(self.table).scalar()