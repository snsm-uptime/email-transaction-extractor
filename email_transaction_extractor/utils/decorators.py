import re
import time
from functools import wraps


def log_method_execution_time(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        self.logger.info(
            f"[EXEC TIME] {func.__name__} = {execution_time} seconds")
        return result
    return wrapper


def clean_whitespace(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Call the original function
        result = func(self, *args, **kwargs)
        # Clean the whitespace
        cleaned_result = re.sub(r'\s+', ' ', result).strip()
        return cleaned_result
    return wrapper
