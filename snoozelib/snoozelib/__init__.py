import re
from typing import List, Tuple
from snoozelib.data_types import DATA_TYPES, NON_DATATYPE_KEYWORDS
from snoozelib.conversion import Conversion
from snoozelib.grpc import GrpcVariable, determine_type_for_grpc
from snoozelib.general import (
    filter_unnecessary_keywords,
    get_data_type,
    get_name_from_sql,
)
from snoozelib.checks import *
from snoozelib.relations import retrofit_relations, M2MAssociationTableInfo


def sql_tables_to_classes(
    sql_sequences: List[str],
) -> Tuple[List[Conversion], List[M2MAssociationTableInfo]]:
    collected_statements = []
    collected_association_tables = []
    for sql in sql_sequences:
        sql_lower: str = sql.lower()
        if not "create table" in sql_lower or not ";" in sql:
            return
        statements = sql_lower.split(";")
        statements = [
            filter_unnecessary_keywords(statement)
            for statement in statements
            if "create table" in statement
        ]
        statements = [_make_class_def(statement) for statement in statements]
        collected_statements += statements

    retrofit_relations(
        sql_sequences=sql_sequences,
        statements=collected_statements,
        association_tables=collected_association_tables,
    )
    [conversion.finalize_sorted_instructions() for conversion in collected_statements]
    return (collected_statements, collected_association_tables)


def _rinse_pre_class_def(sql: str) -> str:
    everything_after_first_bracket: str = re.sub(r"^.+?(?=\()", "", sql)
    return everything_after_first_bracket


def _make_class_def(sql: str) -> Conversion:
    object_name: str = get_name_from_sql(sql)
    variables: List[str] = _rinse_pre_class_def(sql).split(",")
    conversion: Conversion = Conversion(name=object_name)
    for sql_line in variables:

        if not sql_line:
            continue
        if any(
            [keyword.lower() in sql_line.lower() for keyword in NON_DATATYPE_KEYWORDS]
        ):
            continue
        check_reserved_keywords(sql_line.lower())
        sql_line = re.sub(r"[;\n]", "", sql_line)
        data_type: str = get_data_type(sql_line)
        related_data = DATA_TYPES[data_type]
        conversion.concatenate_dependencies(related_data[1])

        code: str = related_data[0]
        code = check_nullable(sql_line, code)
        code = check_unique(sql_line, code)
        code = check_n_value(sql_line, code, data_type)
        var_name = sql_line.replace("(", "").replace(")", "").lstrip().split()[0]
        code = f"{var_name} = {code}"
        if not conversion.grpc_variables:
            conversion.grpc_variables = []
        conversion.grpc_variables.append(
            GrpcVariable(
                var_name=var_name,
                var_type=determine_type_for_grpc(sql_line),
                default="default" in sql_line,
            )
        )
        if not conversion.variable_names:
            conversion.variable_names = []
        conversion.variable_names.append(var_name)
        if not conversion.contents:
            conversion.contents = [code]
        else:
            conversion.contents.append(code)
    return conversion
