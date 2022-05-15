import re
from typing import Dict, List
from data_types import data_types
from custom_exceptions import MultipleDataTypesError, NoSqlDataTypeError
from conversion import Conversion


def sql_tables_to_classes(sql: str) -> List[Conversion]:
    sql_lower: str = sql.lower()
    if not "create table" in sql or not ";" in sql:
        return
    statements: List[str] = sql_lower.split(";")
    statements = [_filter_unnecessary_keywords(
        statement) for statement in statements if "create table" in statement]


def _filter_unnecessary_keywords(sql: str):
    return sql.replace("if not exists", "")


def _get_data_type(sql: str) -> str:
    hit_val: str = ""
    for data_type in data_types.keys():
        if data_type in sql:
            if not hit_val:
                hit_val = data_type
            else:
                raise MultipleDataTypesError(
                    f"sql contained both {hit_val} and {data_type}")
    if not hit_val:
        raise NoSqlDataTypeError(f"No sql data type found in {sql}")
    else:
        return hit_val


def _



def _get_class_def(sql: str) -> dict:
    object_name: str = re.sub(
        r"^.+?(?=create table", sql).replace("create table").split()[0]
    variables: List[str] = sql.split(",")
    obj: dict = {}
    obj['name'] = object_name
