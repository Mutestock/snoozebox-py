from snoozelib import sql_tables_to_classes
import textwrap


def test_translation():
    sql: str = textwrap.dedent(f"""\
    CREATE TABLE whatevs IF NOT EXISTS(
        id SERIAL NOT NULL,
        stuff VARCHAR(255) NOT NULL
    );
    """)
    actual = sql_tables_to_classes(sql)
    expected = 'from sqlalchemy import Integer, Column, String\n\nclass Whatevs(Base):\n    __tablename__: str = "whatevs"\n\n\n    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)\n    stuff = Column(String(255), nullable=False)\n'
    #print(actual[0].resolve_contents())
    assert actual[0].resolve_contents() == expected
    
