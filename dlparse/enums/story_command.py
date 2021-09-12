"""Story command type enum."""
from enum import Enum
from typing import Any

__all__ = ("StoryCommandType",)


class StoryCommandType(Enum):
    """
    Story command type enum.

    There are NO official definitions available. However, except the placeholder for unknown command,
    the strings assigned to all other types of command actually exists.
    """

    UNKNOWN = "(unknown)"

    OUTLINE = "outline"
    """Outline of a story."""

    PRINT = "print"
    """A single text entry."""

    @classmethod
    def _missing_(cls, value: Any) -> "StoryCommandType":
        return StoryCommandType.UNKNOWN
