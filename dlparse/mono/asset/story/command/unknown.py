"""Class for handling unknown story command."""
from dataclasses import dataclass

from dlparse.enums import StoryCommandType
from .base import StoryCommandBase

__all__ = ("StoryCommandUnknown",)


@dataclass
class StoryCommandUnknown(StoryCommandBase):
    """Unknown story command class."""

    @staticmethod
    def expected_type() -> StoryCommandType:
        return StoryCommandType.UNKNOWN
