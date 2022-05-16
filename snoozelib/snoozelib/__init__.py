import re
from typing import List
from snoozelib.data_types import data_types
from snoozelib.custom_exceptions import MissingExpectedValue, MultipleDataTypesError, NoSqlDataTypeError
from snoozelib.conversion import Conversion
from snoozelib.import_instruction import ImportInstruction


def sql_tables_to_classes(sql: str) -> List[Conversion]:
    sql_lower: str = sql.lower()
    if not "create table" in sql or not ";" in sql:
        return
    statements: List[str] = sql_lower.split(";")
    statements = [_filter_unnecessary_keywords(
        statement) for statement in statements if "create table" in statement]
    return [_make_class_def(statement) for statement in statements]


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


def _check_nullable(sql: str, code: str) -> str:
    if 'not null' in sql:
        # Last symbol is assumed to be a parenthesis on Column(Something(), nullable=False -->)<--
        all_but_last_symbol: str = code[:-1]
        all_but_last_symbol += ", nullable=False)"
        return all_but_last_symbol
    else:
        return code


def _check_n_value(sql: str, code: str, data_type: str) -> str:

    if "(n)" in code:
        only_post_data_type: str = re.sub(fr"^.+?(?={data_type})", "", sql)
        contents_inside_brackets: str = re.findall(r"\([^)]*\)", only_post_data_type)[0]
        only_numbers: str = "".join(
            re.findall(r"\d", contents_inside_brackets))
        if not only_numbers:
            raise MissingExpectedValue("No numbers were found post _check_n_value")
        return code.replace("(n)", only_numbers)


def _concatenate_dependencies(conversion: Conversion, dependency_list: List[ImportInstruction]):
    for dependency in dependency_list:
        for current_dependency in conversion.import_instructions:
            if dependency.origin != current_dependency.origin or dependency.import_name != current_dependency.import_name:
                conversion.import_instructions.append(dependency)


def _make_class_def(sql: str) -> Conversion:
    object_name: str = re.sub(
        r"^.+?(?=create table)", "", sql).replace("create table").split()[0]
    variables: List[str] = sql.split(",")
    conversion = Conversion(name=object_name)
    for sql_line in variables:
        data_type: str = _get_data_type(sql_line)
        related_data = data_types[data_type]
        _concatenate_dependencies(conversion, related_data[1])

        code: str = related_data[0]
        code = _check_nullable(sql_line, code)
        code = _check_n_value(sql, code, data_type)
        conversion.contents += code
        
