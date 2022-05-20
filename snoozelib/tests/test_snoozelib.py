from snoozelib import sql_tables_to_classes
import textwrap


def test_translation():
    sql: str = textwrap.dedent(f"""\
    CREATE TABLE whatevs IF NOT EXISTS(
        id SERIAL NOT NULL,
        stuff VARCHAR(255) NOT NULL
    );
    """)
    stuff = sql_tables_to_classes(sql)
    print(stuff)
