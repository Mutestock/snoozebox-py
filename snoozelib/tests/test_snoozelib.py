from snoozelib import sql_tables_to_classes


def test_version():
    sql: str = f"""
    CREATE TABLE whatevs IF NOT EXISTS(
        id SERIAL NOT NULL,
        stuff VARCHAR(255) NOT NULL
    );
    """
    stuff = sql_tables_to_classes(sql)
    print(stuff)
