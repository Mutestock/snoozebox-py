from snoozelib import _determine_type_for_grpc, sql_tables_to_classes
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
    assert actual[0].resolve_contents() == expected
    
    
def test_table_name_contains_keywords():
    sql: str = textwrap.dedent(f""""\
    CREATE TABLE cereal(
        id SERIAL NOT NULL,
        tasty BOOLEAN NOT NULL,
        expired BOOLEAN NOT NULL,
        whatever INTEGER NOT NULL UNIQUE
    );   
    """)
    actual = sql_tables_to_classes(sql)
    assert 'class Cereal(Base):' in actual[0].resolve_contents()
    assert '__tablename__: str = "cereal' in actual[0].resolve_contents()
    
    
def test_unique_gets_added():
    sql: str = textwrap.dedent(f"""\
    CREATE TABLE contains_unique(
        id SERIAL NOT NULL,
        whatever VARCHAR(255) UNIQUE NOT NULL
    );   
    """)
    actual = sql_tables_to_classes(sql)
    assert "unique=True" in actual[0].resolve_contents()
    
    
def test_grpc_types():
    sql: str = textwrap.dedent(f"""\
    CREATE TABLE whatevs IF NOT EXISTS(
        id SERIAL NOT NULL,
        stuff VARCHAR(255) NOT NULL
    );
    """)
    actual = sql_tables_to_classes(sql)
    
    
    
if __name__ == "__main__":
    
    sql: str = textwrap.dedent(f"""\
    CREATE TABLE whatevs IF NOT EXISTS(
        id SERIAL NOT NULL,
        stuff VARCHAR(255) NOT NULL
    );
    """)
    actual = sql_tables_to_classes(sql)
    print(actual[0].grpc_variables)
    #garbage()
    sql_split = sql.split(",")
    for line in sql_split:
        line = line.lower()
        print(_determine_type_for_grpc(line))