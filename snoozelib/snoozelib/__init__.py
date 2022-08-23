import re
from typing import List
from snoozelib.data_types import DATA_TYPES, NON_DATATYPE_KEYWORDS
from snoozelib.custom_exceptions import (
    MalformedSequence,
    MissingTableInRelations,
)
from snoozelib.conversion import Conversion
from snoozelib.grpc import GrpcVariable, determine_type_for_grpc
from snoozelib.import_instruction import ImportInstruction
from snoozelib.general import (
    filter_unnecessary_keywords,
    get_next_word,
    get_contents_inside_brackets,
    get_data_type,
    get_name_from_sql,
)
from snoozelib.checks import *


def sql_tables_to_classes(sql_sequences: List[str]) -> List[Conversion]:
    collected_statements = []
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

    _retrofit_relations(sql_sequences=sql_sequences, statements=collected_statements)
    return collected_statements


def _retrofit_relations(sql_sequences: List[str], statements: List[Conversion]):
    lowered_sequences: List[str] = [
        filter_unnecessary_keywords(sequence.lower()) for sequence in sql_sequences
    ]
    for sequence in lowered_sequences:
        if not "references" in sequence or not "foreign key" in sequence:
            continue
        name = get_next_word(
            sql=sequence,
            search_words="create table",
        ).replace("(", "")
        references = get_next_word(sql=sequence, search_words="references")
        foreign_key_id = get_next_word(sql=sequence, search_words="foreign key")
        reference_id = (
            get_contents_inside_brackets(references)[0]
            .replace("(", "")
            .replace(")", "")
        )
        reference_table_name = references.split("(", maxsplit=1)[0]

        if all([name, references, foreign_key_id, reference_id, reference_table_name]):
            conversion01 = None
            conversion02 = None
            for conversion in statements:
                if conversion.name == name:
                    conversion01 = conversion
                elif conversion.name == reference_table_name:
                    conversion02 = conversion
            if not conversion01:
                raise MissingTableInRelations(
                    f"Table {name} wasn't found in relations retrofit. Tell the dev he's stupid, since this isn't supposed to happen."
                )
            if not conversion02:
                raise MissingTableInRelations(
                    f"No table with the name {reference_table_name} was found. Are you sure you've created a table with such a name?"
                )
            conversion01.import_instructions.append(
                ImportInstruction(origin="sqlalchemy.orm", import_name="backref")
            )
            conversion01.import_instructions.append(
                ImportInstruction(origin="sqlalchemy.orm", import_name="relationship")
            )

        else:
            raise MalformedSequence(f"The line: {sequence} is considered malformed")


def _rinse_pre_class_def(sql: str) -> str:
    everything_after_first_bracket = re.sub(r"^.+?(?=\()", "", sql)
    return everything_after_first_bracket


def _make_class_def(sql: str) -> Conversion:
    object_name: str = get_name_from_sql(sql)
    variables: List[str] = _rinse_pre_class_def(sql).split(",")
    conversion = Conversion(name=object_name)
    for sql_line in variables:
        if not sql_line:
            continue
        if any(
            [keyword.lower() in sql_line.lower() for keyword in NON_DATATYPE_KEYWORDS]
        ):
            continue
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
    conversion.finalize_sorted_instructions()
    return conversion
