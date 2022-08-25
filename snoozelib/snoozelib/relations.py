from dataclasses import dataclass
from snoozelib.conversion import Conversion
from snoozelib.custom_exceptions import (
    MissingTableInRelations,
    MalformedSequence,
    RelationsOutsideBounds,
)
from snoozelib.general import (
    get_next_word,
    get_contents_inside_brackets,
    filter_unnecessary_keywords,
)
from snoozelib.import_instruction import ImportInstruction

from enum import Enum
from typing import List, Tuple


@dataclass
class M2MAssociationTableInfo:
    name: str
    ref_table_name01: str
    ref_table_name02: str
    fkey01: str
    fkey02: str

    def __init__(self, sequence: str):
        seq_clone: str = sequence
        hits: int = 0
        for line in seq_clone.split(","):
            if not sequence_related_to_relations(line):
                continue
            else:
                hits += 1
            if hits == 0:
                raise RelationsOutsideBounds("This is not supposed to happen")
            elif hits == 1:
                self.ref_table_name01 = _extract_ref_name(line)
                self.fkey01 = _extract_fkey(line)
            elif hits == 2:
                self.ref_table_name02 = _extract_ref_name(line)
                self.fkey02 = _extract_fkey(line)
            else:
                raise RelationsOutsideBounds(
                    "There were more than two references or foreign keys inside a table definition. Snoozebox isn't smart enough for that. Sorry."
                )
        self.name = f"{self.ref_table_name01}_{self.ref_table_name02}"

        if not all(
            [
                self.name,
                self.ref_table_name01,
                self.ref_table_name02,
                self.fkey01,
                self.fkey02,
            ]
        ):
            raise MalformedSequence(f"The line: {sequence} is considered malformed")


@dataclass
class RelationSqlInfo:
    name: str
    reference: str
    foreign_key_id: str
    reference_id: str
    reference_table_name: str

    def __init__(self, sequence: str):
        self.name = _extract_table_name(sequence)
        self.references = get_next_word(sql=sequence, search_words="references")
        self.foreign_key_id = _extract_fkey(sequence)
        self.reference_id = (
            get_contents_inside_brackets(self.references)[0]
            .replace("(", "")
            .replace(")", "")
        )
        self.reference_table_name = _extract_ref_name(sequence)

        if not all(
            [
                self.name,
                self.references,
                self.foreign_key_id,
                self.reference_id,
                self.reference_table_name,
            ]
        ):
            raise MalformedSequence(f"The line: {sequence} is considered malformed")


class Relation(Enum):
    NONE = 1
    ONE_TO_MANY = 2
    MANY_TO_MANY = 3


def _extract_table_name(sequence) -> str:
    return get_next_word(
        sql=sequence,
        search_words="create table",
    ).replace("(", "")


def _extract_ref_name(sequence: str) -> str:
    return get_next_word(sql=sequence, search_words="references").split(
        "(", maxsplit=1
    )[0]


def _extract_fkey(sequence: str) -> str:
    fkey = get_next_word(sql=sequence, search_words="foreign key")
    if "(" in fkey:
        fkey = fkey.split("(", maxsplit=1)[0]
    return fkey


def one_to_many(lowered_sequences: List[str], statements: List[Conversion]) -> None:
    for sequence in lowered_sequences:
        if not sequence_related_to_relations(sequence):
            continue
        relation_sql_info: RelationSqlInfo = RelationSqlInfo(sequence=sequence)

        (conversion01, conversion02) = o2m_conversions_collection(
            statements=statements, relation_sql_info=relation_sql_info
        )
        conversion01.import_instructions.append(
            ImportInstruction(origin="sqlalchemy.orm", import_name="relationship")
        )
        conversion01.contents.append(
            f'{conversion02.name}s = relationship("{relation_sql_info.reference_table_name}")'
        )
        conversion02.import_instructions.append(
            ImportInstruction(origin="sqlalchemy", import_name="ForeignKey")
        )
        conversion02.contents.append(
            f'{relation_sql_info.reference_table_name}_{relation_sql_info.reference_id} = Column(Integer, ForeignKey("{relation_sql_info.name}.{relation_sql_info.foreign_key_id}"))'
        )


def o2m_conversions_collection(
    statements: List[Conversion], relation_sql_info: RelationSqlInfo
) -> Tuple[Conversion, Conversion]:
    conversion01: Conversion = None
    conversion02: Conversion = None
    for conversion in statements:
        if conversion.name == relation_sql_info.name:
            conversion01 = conversion
        elif conversion.name == relation_sql_info.reference_table_name:
            conversion02 = conversion
    if not conversion01:
        raise MissingTableInRelations(
            f"Table {relation_sql_info.name} wasn't found in relations retrofit. Tell the dev he's stupid, since this isn't supposed to happen."
        )
    if not conversion02:
        raise MissingTableInRelations(
            f"No table with the name {relation_sql_info.reference_table_name} was found. Are you sure you've created a table with such a name?"
        )
    return (conversion01, conversion02)



def many_to_many(
    lowered_sequences: List[str],
    statements: List[Conversion],
    association_tables: List[M2MAssociationTableInfo],
) -> None:
    for sequence in lowered_sequences:
        if not sequence_related_to_relations(sequence):
            continue
        m2m_association_table = M2MAssociationTableInfo(sequence=sequence)
        (conversion01, conversion02) = m2m_conversions_collection(
            statements, m2m_association_table, sequence
        )

        conversion01.import_instructions.append(
            ImportInstruction(origin="sqlalchemy.orm", import_name="relationship")
        )
        conversion01.import_instructions.append(
            ImportInstruction(
                origin="models.association_tables",
                import_name=f"{m2m_association_table.name}",
            )
        )
        conversion01.contents.append(
            f'{conversion02.name}s = relationship("{conversion02.name}", secondary={m2m_association_table.name})'
        )
        association_tables.append(m2m_association_table)


def sequence_related_to_relations(sequence: str) -> bool:
    if "references" in sequence or "foreign key" in sequence:
        return True


def m2m_conversions_collection(
    statements: List[Conversion],
    m2m_association_table: M2MAssociationTableInfo,
    sequence: str,
) -> Tuple[Conversion, Conversion]:
    conversion01: Conversion = None
    conversion02: Conversion = None
    conversion_to_remove: Conversion = None
    for conversion in statements:
        if conversion.name == m2m_association_table.ref_table_name01:
            conversion01 = conversion
        elif conversion.name == m2m_association_table.ref_table_name02:
            conversion02 = conversion
        elif conversion.name == m2m_association_table.name:
            conversion_to_remove = conversion
    statements.remove(conversion_to_remove)
    if not conversion01 and not conversion02:
        raise MissingTableInRelations(
            f"""Neither a table of name {m2m_association_table.ref_table_name01} nor a table of name {m2m_association_table.ref_table_name02} was found. 
            Association table {m2m_association_table.name} failed. 
            Faulty sequence: 
            {sequence}
            
            Aborting..."""
        )
    if not conversion01:
        raise MissingTableInRelations(
            f"""Table of name {m2m_association_table.ref_table_name01} not found
            Association table {m2m_association_table.name} failed. 
            Faulty sequence:
            {sequence}
            
            Aborting..."""
        )
    if not conversion02:
        raise MissingTableInRelations(
            f"""Table of name {m2m_association_table.ref_table_name02} not found
            Association table {m2m_association_table.name} failed. 
            Faulty sequence:
            {sequence}
            
            Aborting..."""
        )
    if not conversion_to_remove:
        raise MissingTableInRelations(
            f"""No conversion was removed during many to many process. 
            This is a programming error from the developer of snoozelib's part
            Tell the snoozebox dev he's dumb
            
            Faulty sequence:
            {sequence}
            
            Aborting..."""
        )
    return (conversion01, conversion02)



def discover_relations(sql_sequences: List[str]) -> Relation:
    hits: int = 0
    for sequence in sql_sequences:
        if sequence_related_to_relations(sequence):
            hits += 1
    if hits == 0:
        return Relation.NONE
    elif hits == 1:
        return Relation.ONE_TO_MANY
    elif hits == 2:
        return Relation.MANY_TO_MANY
    else:
        raise RelationsOutsideBounds(
            "There were more than two references or foreign keys inside a table definition. Snoozebox isn't smart enough for that. Sorry."
        )


def retrofit_relations(
    sql_sequences: List[str],
    statements: List[Conversion],
    association_tables: List[M2MAssociationTableInfo],
) -> None:
    if len(statements) < 2:
        return
    lowered_sequences: List[str] = [
        filter_unnecessary_keywords(sequence.lower()) for sequence in sql_sequences
    ]
    
    for sequence in lowered_sequences:
        sequence_lines = sequence.split(",")
        relation_strategy: Relation = discover_relations(sequence_lines)
        if relation_strategy == Relation.NONE:
            continue
        elif relation_strategy == Relation.ONE_TO_MANY:
            one_to_many(lowered_sequences, statements)
        elif relation_strategy == Relation.MANY_TO_MANY:
            many_to_many(lowered_sequences, statements, association_tables)
        else:
            raise RelationsOutsideBounds(
                """There were more than two references or foreign keys inside a table definition. Snoozebox isn't smart enough for that. Sorry. 
                This particular result isn't supposed to happen, by the way. Inform the programmer that he sucks immediately."""
            )
