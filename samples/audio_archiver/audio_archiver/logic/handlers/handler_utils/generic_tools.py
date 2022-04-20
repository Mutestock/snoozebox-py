
# Maybe a bit silly, but I'm thinking it's a constant so we might as well?
SUCCESFUL_TRANSACTION = "Ok"

def make_error_message(ex: Exception) -> str:
    return f"Err {ex}"