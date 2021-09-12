"""Error classes used when processing stories."""
from .base import AppValueError

__all__ = ("StoryUnavailableError",)


class StoryUnavailableError(AppValueError):
    """Error to be raised if the story is unavailable."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
