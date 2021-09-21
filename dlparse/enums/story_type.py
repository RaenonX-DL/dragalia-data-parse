"""Enums for the story type."""
from enum import Enum, auto

__all__ = ("StoryType",)


class StoryType(Enum):
    """
    Story type enum.

    No official definitions as this is a custom type.
    """

    UNIT = auto()
    QUEST = auto()
    CASTLE = auto()
