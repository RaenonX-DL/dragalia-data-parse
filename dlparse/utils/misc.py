"""Miscellaneous utility functions."""
import time
from functools import wraps

__all__ = ("time_exec",)


def time_exec(title: str):
    """Decorator to time the function execution time."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _start = time.time()
            ret = fn(*args, **kwargs)
            print(f"{title}: {time.time() - _start:.3f} secs")
            return ret

        return wrapper

    return decorator
