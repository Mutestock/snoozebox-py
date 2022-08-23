from snoozelib.conversion import Conversion
from snoozelib.custom_exceptions import MissingTableInRelations
from typing import List, Tuple


def one_to_many():
    pass


def many_to_many():
    pass


def sequence_related_to_relations(sequence: str) -> bool:
    if "references" in sequence or "foreign key" in sequence:
        return True


def conversions_collection(
    statements: List[Conversion], name: str, reference_table_name: str
) -> Tuple[Conversion, Conversion]:
    conversion01: Conversion = None
    conversion02: Conversion = None
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
    return (conversion01, conversion02)
