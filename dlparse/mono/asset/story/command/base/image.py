"""Story command class for the command containing an image code."""
from abc import abstractmethod
from dataclasses import dataclass

from .base import StoryCommandBase

__all__ = ("StoryCommandHasImage",)


@dataclass
class StoryCommandHasImage(StoryCommandBase):
    """Story command that has an image."""

    @property
    @abstractmethod
    def image_code(self) -> str:
        """Image code of the command."""
        raise NotImplementedError()
