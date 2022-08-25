from snoozelib.custom_exceptions import MissingExpectedValue, ReservedKeyword
from snoozelib.general import get_only_numbers
from snoozelib.data_types import RESERVED_KEYWORDS


def check_keyword(sql: str, code: str, keyword: str, to_add: str) -> str:
    if keyword in sql:
        # Last symbol is assumed to be a parenthesis on Column(Something(), nullable=False -->)<--
        all_but_last_symbol: str = code[:-1]
        all_but_last_symbol += to_add
        return all_but_last_symbol
    else:
        return code


def check_nullable(sql: str, code: str) -> str:
    return check_keyword(
        sql=sql, code=code, keyword="not null", to_add=", nullable=False)"
    )


def check_unique(sql: str, code: str) -> str:
    return check_keyword(sql=sql, code=code, keyword="unique", to_add=", unique=True)")


def check_n_value(sql: str, code: str, data_type: str) -> str:

    if "(n)" in code:
        only_numbers: str = get_only_numbers(sql, data_type)
        if not only_numbers:
            raise MissingExpectedValue("No numbers were found post check_n_value")
        return code.replace("(n)", "(" + only_numbers + ")")
    else:
        return code


def check_reserved_keywords(sql: str) -> None:
    for keyword in RESERVED_KEYWORDS:
        if keyword in sql:
            raise ReservedKeyword(
                f"""'{keyword}' is a reserved keyword and thus cannot be used inside data structures.    
                
                Faulty sql:
                {sql}
                
                Aborting...
                """
            )
