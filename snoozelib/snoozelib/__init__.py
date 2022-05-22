import re
from typing import List
from snoozelib.data_types import data_types
from snoozelib.custom_exceptions import (
    MissingExpectedValue,
    MultipleDataTypesError,
    NoSqlDataTypeError,
)
from snoozelib.conversion import Conversion
from snoozelib.grpc_variable import GrpcVariable


def sql_tables_to_classes(sql: str) -> List[Conversion]:
    sql_lower: str = sql.lower()
    if not "create table" in sql_lower or not ";" in sql:
        return
    statements: List[str] = sql_lower.split(";")
    statements = [
        _filter_unnecessary_keywords(statement)
        for statement in statements
        if "create table" in statement
    ]
    statements = [_make_class_def(statement) for statement in statements]
    return statements


def _filter_unnecessary_keywords(sql: str):
    return sql.replace("if not exists", "")


def _get_data_type(sql: str) -> str:
    hit_val: str = ""
    for data_type in data_types.keys():
        dtype_mod: str = data_type
        if "(n)" in dtype_mod:
            dtype_mod = data_type.replace(("(n)"), "")
        for word in sql.split():
            if "(" in word and ")" in word:
                only_numbers = _get_only_numbers(sql, data_type)
                word = word.replace(only_numbers, "n")
            if data_type == word:
                if not hit_val:
                    hit_val = data_type
                else:
                    raise MultipleDataTypesError(
                        f"sql contained both {hit_val} and {data_type}"
                    )
    if not hit_val:
        raise NoSqlDataTypeError(f"No sql data type found in {sql}")
    else:
        return hit_val


def _check_keyword(sql: str, code: str, keyword: str, to_add: str) -> str:
    if keyword in sql:
        # Last symbol is assumed to be a parenthesis on Column(Something(), nullable=False -->)<--
        all_but_last_symbol: str = code[:-1]
        all_but_last_symbol += to_add
        return all_but_last_symbol
    else:
        return code


def _check_nullable(sql: str, code: str) -> str:
    return _check_keyword(
        sql=sql, code=code, keyword="not null", to_add=", nullable=False)"
    )


def _check_unique(sql: str, code: str) -> str:
    return _check_keyword(sql=sql, code=code, keyword="unique", to_add=", unique=True)")


def _get_only_numbers(sql: str, data_type: str) -> str:
    only_post_data_type: str = re.sub(rf"^.+?(?={data_type})", "", sql)
    contents_inside_brackets: str = re.findall(r"\([^)]*\)", only_post_data_type)[0]
    only_numbers: str = "".join(re.findall(r"\d", contents_inside_brackets))
    return only_numbers


def _check_n_value(sql: str, code: str, data_type: str) -> str:

    if "(n)" in code:
        only_numbers: str = _get_only_numbers(sql, data_type)
        if not only_numbers:
            raise MissingExpectedValue("No numbers were found post _check_n_value")
        return code.replace("(n)", "(" + only_numbers + ")")
    else:
        return code


def _rinse_pre_class_def(sql: str) -> str:
    everything_after_first_bracket = re.sub(r"^.+?(?=\()", "", sql)
    return everything_after_first_bracket


def _determine_type_for_grpc(sql_line: str) -> str:
    dtype = _get_data_type(sql_line)
    if dtype in [
        "bigint",
        "int8",
        "bigserial",
        "serial8",
        "bit",
        "bit_varying",
        "bytea",
        "double precision",
        "float8",
        "integer",
        "int",
        "int4",
        "real",
        "float4",
        "smallint",
        "int2",
        "smallserial",
        "serial2",
        "serial",
        "serial4",
    ]:
        return "int32"
    elif dtype in ["bool", "boolean"]:
        return "bool"
    else:
        return "str"

def _make_class_def(sql: str) -> Conversion:
    object_name: str = (
        re.sub(r"^.+?(?=create table)", "", sql).replace("create table", "").split()[0]
    ).replace("(", "")
    variables: List[str] = _rinse_pre_class_def(sql).split(",")
    conversion = Conversion(name=object_name)
    for sql_line in variables:
        if not sql_line:
            continue
        sql_line = re.sub(r"[;\n]", "", sql_line)
        data_type: str = _get_data_type(sql_line)
        related_data = data_types[data_type]
        conversion.concatenate_dependencies(related_data[1])

        code: str = related_data[0]
        code = _check_nullable(sql_line, code)
        code = _check_unique(sql_line, code)
        code = _check_n_value(sql_line, code, data_type)
        var_name = sql_line.replace("(", "").replace(")", "").lstrip().split()[0]
        code = f"{var_name} = {code}\n"
        if not conversion.grpc_variables:
            conversion.grpc_variables = []
        conversion.grpc_variables.append(
            GrpcVariable(var_name=var_name, var_type=_determine_type_for_grpc(sql_line), default="default" in sql_line)
        )
        if not conversion.variable_names:
            conversion.variable_names = []
        conversion.variable_names.append(var_name)
        if not conversion.contents:
            conversion.contents = code
        else:
            conversion.contents += code
    conversion.resolve_contents()
    return conversion
