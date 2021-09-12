"""Error classes used when processing stories."""
from .base import AppValueError

__all__ = ("StoryUnavailableError",)


class StoryUnavailableError(AppValueError):
    """Error to be raised if the story is unavailable."""
