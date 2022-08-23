import re
from typing import List
from snoozelib.data_types import DATA_TYPES, NON_DATATYPE_KEYWORDS
from snoozelib.custom_exceptions import (
    MalformedSequence,
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
from snoozelib.relations import sequence_related_to_relations, conversions_collection


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
    [conversion.finalize_sorted_instructions() for conversion in collected_statements]
    return collected_statements


def _retrofit_relations(sql_sequences: List[str], statements: List[Conversion]) -> None:
    lowered_sequences: List[str] = [
        filter_unnecessary_keywords(sequence.lower()) for sequence in sql_sequences
    ]
    for sequence in lowered_sequences:
        if not sequence_related_to_relations(sequence=sequence):
            continue
        name: str = get_next_word(
            sql=sequence,
            search_words="create table",
        ).replace("(", "")
        references: str = get_next_word(sql=sequence, search_words="references")
        foreign_key_id: str = get_next_word(sql=sequence, search_words="foreign key")
        reference_id: str = (
            get_contents_inside_brackets(references)[0]
            .replace("(", "")
            .replace(")", "")
        )
        reference_table_name: str = references.split("(", maxsplit=1)[0]

        if all([name, references, foreign_key_id, reference_id, reference_table_name]):
            (conversion01, conversion02) = conversions_collection(
                statements=statements,
                name=name,
                reference_table_name=reference_table_name,
            )
            conversion01.import_instructions.append(
                ImportInstruction(origin="sqlalchemy.orm", import_name="relationship")
            )
            conversion01.contents.append(
                f'{conversion02.name}s = relationship("{reference_table_name}")'
            )
            conversion02.import_instructions.append(ImportInstruction(origin="sqlalchemy", import_name="ForeignKey"))
            conversion02.contents.append(
                f'{reference_table_name}_{reference_id} = Column(Integer, ForeignKey("{name}.{foreign_key_id}"))'
            )
        else:
            raise MalformedSequence(f"The line: {sequence} is considered malformed")


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
