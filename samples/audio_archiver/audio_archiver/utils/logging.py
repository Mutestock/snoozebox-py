import logging
import os
from utils.config import LOG_FILE_PATH

def setup_logger():
    if not os.path.exists(LOG_FILE_PATH):
        os.mkdir(LOG_FILE_PATH)
    logging.basicConfig(filename=f"{LOG_FILE_PATH}/log.log", encoding='utf-8', level=logging.DEBUG)
    
def decoration_logger(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error caught by decoration logger on function: {func.__name__} of type: {type(e)} with message: {e}")
    
    return wrapper