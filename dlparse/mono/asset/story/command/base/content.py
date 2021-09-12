"""Class for a story command that contains a text content."""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .base import StoryCommandBase

__all__ = ("StoryCommandHasContent",)


@dataclass
class StoryCommandHasContent(StoryCommandBase, ABC):
    """A story command that contains a text content."""

    @property
    @abstractmethod
    def content(self) -> str:
        raise NotImplementedError()
