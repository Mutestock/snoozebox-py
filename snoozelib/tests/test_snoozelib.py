from typing import List
from snoozelib import sql_tables_to_classes
from snoozelib.conversion import Conversion
import textwrap


def test_translation():
    sql: str = textwrap.dedent(
        f"""\
    CREATE TABLE whatevs IF NOT EXISTS(
        id SERIAL NOT NULL,
        stuff VARCHAR(255) NOT NULL
    );
    """
    )
    (actual, _) = sql_tables_to_classes([sql])
    expected1 = (
        "id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)"
    )
    expected2 = "stuff = Column(String(255), nullable=False)"
    assert expected1 in actual[0].contents[0]
    assert expected2 in actual[0].contents[1]


def test_table_name_contains_keywords():
    sql: str = textwrap.dedent(
        f""""\
    CREATE TABLE cereal(
        id SERIAL NOT NULL,
        tasty BOOLEAN NOT NULL,
        expired BOOLEAN NOT NULL,
        whatever INTEGER NOT NULL UNIQUE
    );   
    """
    )
    (actual, _) = sql_tables_to_classes([sql])
    assert "nullable=False" in actual[0].contents[0]


def test_unique_gets_added():
    sql: str = textwrap.dedent(
        f"""\
    CREATE TABLE contains_unique(
        id SERIAL NOT NULL,
        whatever VARCHAR(255) UNIQUE NOT NULL
    );   
    """
    )
    (actual, _) = sql_tables_to_classes([sql])
    assert "unique=True" in actual[0].contents[1]


def test_grpc_types():
    sql: str = textwrap.dedent(
        f"""\
    CREATE TABLE whatevs IF NOT EXISTS(
        id SERIAL NOT NULL,
        stuff VARCHAR(255) NOT NULL
    );
    """
    )
    (actual, _) = sql_tables_to_classes([sql])


def test_conversion_sorted_instructions_has_multiple_values():
    sql: str = textwrap.dedent(
        f"""\
    CREATE TABLE contains_unique(
        id SERIAL NOT NULL,
        whatever VARCHAR(255) UNIQUE NOT NULL
    );   
    """
    )
    (res, _) = sql_tables_to_classes([sql])
    hit_of_over_one_vars: bool = False
    for conversion in res:
        for sorted_instruction in conversion.sorted_import_instructions:
            if len(sorted_instruction.imports) > 1:
                hit_of_over_one_vars = True
    assert hit_of_over_one_vars == True


def test_no_new_lines():
    sql: str = textwrap.dedent(
        f"""\
    CREATE TABLE contains_unique(
        id SERIAL NOT NULL,
        whatever VARCHAR(255) UNIQUE NOT NULL
    );   
    """
    )
    (res, _) = sql_tables_to_classes([sql])
    hit: bool = False
    for conversion in res:
        for content in conversion.contents:
            if "\n" in content:
                hit = True
    assert hit == False


def test_relations() -> None:
    sql01: str = textwrap.dedent(
        f"""\
    CREATE TABLE contains_unique(
        id SERIAL NOT NULL,
        whatever VARCHAR(255) UNIQUE NOT NULL,
        FOREIGN KEY uid REFERENCES some_table(uid)
    );   
    """
    )
    sql02: str = textwrap.dedent(
        f"""\
    CREATE TABLE some_table(
        uid SERIAL NOT NULL,
        name VARCHAR(255) UNIQUE NOT NULL
    );   
    """
    )
    (res, _) = sql_tables_to_classes([sql01, sql02])


def test_examples() -> None:
    """
    This tests the examples generated with Jinja as per 25/08/22
    """
    o2m01: str = """
    CREATE TABLE IF NOT EXISTS person(
        id SERIAL NOT NULL,
        name VARCHAR(255) UNIQUE NOT NULL,
        age INT NOT NULL,
        occupied BOOL NOT NULL
    );
    """
    o2m02: str = """
    CREATE TABLE IF NOT EXISTS company(
        id SERIAL NOT NULL,
        title VARCHAR(255) UNIQUE NOT NULL
    );
    """

    m2m01: str = """
    CREATE TABLE IF NOT EXISTS tag(
        id SERIAL NOT NULL,
        name VARCHAR(100) UNIQUE NOT NULL
    );  
    """

    m2m02: str = """
    CREATE TABLE IF NOT EXISTS msg(
        id SERIAL NOT NULL,
        contents VARCHAR(5000) NOT NULL
    );
    """

    m2mAssoc: str = """
    CREATE TABLE IF NOT EXISTS tag_msg(
        FOREIGN KEY tag_id REFERENCES tag(id),
        FOREIGN KEY msg_id REFERENCES msg(id)
    );
    """
    (conversions, associations) = sql_tables_to_classes(
        [o2m01, o2m02, m2m01, m2m02, m2mAssoc]
    )
    assert conversions != None
    assert associations != None


def test_duplicate_table_name() -> None:
    pass
