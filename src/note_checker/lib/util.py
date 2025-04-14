import time
import functools
from typing import Callable, Type, TypeVar
from venv import logger

F = TypeVar("F", bound=Callable)

def backoff_on_exception(exception_type: Type[BaseException], max_attempts: int = 10, base_delay: float = 5.0) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exception_type as e:
                    logger.warning(f"Hit rate limit. Backing off for {delay} seconds.")
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
                    delay *= 2
        return wrapper  # type: ignore
    return decorator
