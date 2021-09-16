"""Error classes used when processing stories."""
from .base import AppValueError

__all__ = ("StoryUnavailableError", "StorySpeakerNameNotFoundError")


class StoryUnavailableError(AppValueError):
    """Error to be raised if the story is unavailable."""


class StorySpeakerNameNotFoundError(AppValueError):
    """Error to be raised if the story speaker name is unavailable."""
