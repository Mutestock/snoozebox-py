# Converts some SQL into a string representation of a Python class which implements sqlalchemy


def _contains_create_table_command(sql: str) -> bool:
    return "CREATE TABLE" in sql


def _contains_and_ends_with_brackets(sql: str) -> bool:
    return ("(" in sql and sql[-1:-2] == ");")


def _remove_irrelevant_elements(sql: str) -> str:
    return sql.replace("IF EXISTS", "")


def _get_table_name(sql: str) -> str:
    if _contains_create_table_command(sql):
        fmt = _remove_irrelevant_elements(sql)
        split = fmt.split(" ")
        if 3 > len(split) and not _contains_and_ends_with_brackets(sql):
            raise Exception("Not enough elements in list. No table to create")

        for i, part in enumerate(split):
            if part == "CREATE":
                return (
                    split[i+2]
                    .replace("(", "")
                    .replace("\n", "")
                )

        raise Exception(
            "Somehow now table was found after enumeration. This should never happen")
    else:
        raise Exception(
            "No 'CREATE TABLE' was found in the provided sql. Aborting...")


def parse_table():
    pass
