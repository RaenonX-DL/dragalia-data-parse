"""Miscellaneous utility functions."""
import time
from functools import wraps
from typing import Any, Sequence, TypeVar

__all__ = ("time_exec", "remove_duplicates_preserve_order")


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


T = TypeVar("T", bound=Sequence[Any])


def remove_duplicates_preserve_order(seq: T) -> T:
    """
    Remove the duplicates in ``seq`` while preserving the sequential order.

    Copied from https://stackoverflow.com/a/17016257/11571888.
    """
    seq_type = type(seq)

    return seq_type(dict.fromkeys(seq))
