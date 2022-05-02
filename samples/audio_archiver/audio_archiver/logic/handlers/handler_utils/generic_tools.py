from datetime import datetime

# Maybe a bit silly, but I'm thinking it's a constant so we might as well?
SUCCESFUL_TRANSACTION = "Ok"


def make_error_message(ex: Exception) -> str:
    return f"Err {ex}"


def prepare_object_for_querying(obj: object) -> dict:
    return {
        key: value
        for (key, value) in obj.__dict__.items()
        if value != None and key != "_sa_instance_state"
    }

def iter_parse_datetime(some_dict: dict) -> dict:
    intermediate = {}
    for key, value in some_dict.items():
        if type(value) == datetime:
            intermediate[key]=str(value)
        else:
            intermediate[key]=value
    return intermediate