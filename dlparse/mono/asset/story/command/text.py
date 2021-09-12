"""Story command class for `print`."""
from dataclasses import dataclass

from .base import StoryCommandHasContent

__all__ = ("StoryCommandPrintText",)


@dataclass
class StoryCommandPrintText(StoryCommandHasContent):
    """
    A story command that prints some text.

    - 1st argument: speaker's name
    - 2nd argument: the story content
    - 3rd argument (optional): voice label
    """

    @property
    def content(self) -> str:
        return self.args[1]
