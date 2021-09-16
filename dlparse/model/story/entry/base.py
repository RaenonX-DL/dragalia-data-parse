"""Base classes for story entry."""
from dataclasses import dataclass

__all__ = ("StoryEntryBase",)


@dataclass
class StoryEntryBase:
    """Base class of an entry of a story conversation."""
