import time
import functools
from typing import Callable, Type, TypeVar
from venv import logger

F = TypeVar("F", bound=Callable)


def backoff_on_exception(
    exception_type: Type[BaseException], max_attempts: int = 10, base_delay: float = 5.0
) -> Callable[[F], F]:
    """
    Decorator that retries a function with exponential backoff when a specified exception is raised.

    Args:
        exception_type (Type[BaseException]): The exception type to catch and retry on.
        max_attempts (int): Maximum number of attempts before giving up. Defaults to 10.
        base_delay (float): Initial delay in seconds before retrying. Doubles on each failure. Defaults to 5.0.

    Returns:
        Callable[[F], F]: The decorated function with retry logic.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exception_type:
                    logger.warning(f"Hit rate limit. Backing off for {delay} seconds.")
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
                    delay *= 2

        return wrapper  # type: ignore

    return decorator
