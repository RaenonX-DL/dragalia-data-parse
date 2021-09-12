"""Story command class for `print`3"""
from dataclasses import dataclass

from dlparse.enums import StoryCommandType
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

    @staticmethod
    def expected_type() -> StoryCommandType:
        return StoryCommandType.PRINT

    @property
    def content(self) -> str:
        return self.args[1]
