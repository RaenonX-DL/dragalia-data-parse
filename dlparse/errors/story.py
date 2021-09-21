"""Error classes used when processing stories."""
from typing import Any

from .base import AppValueError

__all__ = (
    "StoryUnavailableError", "StorySpeakerNameNotFoundError", "StoryImageNotFoundError", "UnknownStoryTypeError"
)


class StoryUnavailableError(AppValueError):
    """Error to be raised if the story is unavailable."""


class StorySpeakerNameNotFoundError(AppValueError):
    """Error to be raised if the story speaker name is unavailable."""


class StoryImageNotFoundError(AppValueError):
    """Error to be raised if the story image is unavailable."""


class UnknownStoryTypeError(AppValueError):
    """Error to be raised if the story type is unknown/unhandled."""

    def __init__(self, story_type: Any):
        super().__init__(f"Unknown/unhandled story type: {story_type}")
