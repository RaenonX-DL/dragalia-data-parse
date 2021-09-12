"""Class for handling unknown story command."""
from dataclasses import dataclass

from .base import StoryCommandBase

__all__ = ("StoryCommandUnknown",)


@dataclass
class StoryCommandUnknown(StoryCommandBase):
    """Unknown story command class."""
