import re
from snoozelib.data_types import DATA_TYPES, NON_DATATYPE_KEYWORDS
from snoozelib.custom_exceptions import NoSqlDataTypeError, MultipleDataTypesError
from typing import List


def get_name_from_sql(sql: str) -> str:
    return (
        re.sub(r"^.+?(?=create table)", "", sql).replace("create table", "").split()[0]
    ).replace("(", "")


def get_next_word(sql: str, search_words: str) -> str:
    return sql.split(search_words, maxsplit=1)[-1].split(maxsplit=1)[0]


def get_only_numbers(sql: str, data_type: str) -> str:
    only_post_data_type: str = re.sub(rf"^.+?(?={data_type})", "", sql)
    contents_inside_brackets: str = re.findall(r"\([^)]*\)", only_post_data_type)[0]
    only_numbers: str = "".join(re.findall(r"\d", contents_inside_brackets))
    return only_numbers


def get_data_type(sql: str) -> str:
    hit_val: str = ""
    for data_type in DATA_TYPES.keys():
        dtype_mod: str = data_type
        if "(n)" in dtype_mod:
            dtype_mod = data_type.replace(("(n)"), "")
        for word in sql.split():
            if "(" in word and ")" in word:
                only_numbers = get_only_numbers(sql, data_type)
                word = word.replace(only_numbers, "n")
            if data_type == word:
                if not hit_val:
                    hit_val = data_type
                else:
                    raise MultipleDataTypesError(
                        f"sql contained both {hit_val} and {data_type}"
                    )
    if not hit_val:
        other_keyword_hit: bool = False
        for keyword in NON_DATATYPE_KEYWORDS:
            if keyword.lower() in sql.lower():
                other_keyword_hit = True
        if not other_keyword_hit:
            raise NoSqlDataTypeError(f"No sql data type found in {sql}")
    else:
        return hit_val


def get_contents_inside_brackets(string_to_retrieve_contents_from: str) -> List[str]:
    return re.findall(r"\([^)]*\)", string_to_retrieve_contents_from)


def filter_unnecessary_keywords(sql: str):
    return sql.replace("if not exists", "")
