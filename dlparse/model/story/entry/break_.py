"""Class for story entry representing a thematic break."""
from dataclasses import dataclass

from .base import StoryEntryBase

__all__ = ("StoryEntryBreak",)


@dataclass
class StoryEntryBreak(StoryEntryBase):
    """A single story thematic break."""

    def __repr__(self) -> str:
        return "-" * 20
