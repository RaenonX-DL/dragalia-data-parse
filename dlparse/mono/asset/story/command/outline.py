"""Story command class for `outline`."""
from dataclasses import dataclass

from dlparse.enums import StoryCommandType
from .base import StoryCommandHasContent

__all__ = ("StoryCommandOutline",)


@dataclass
class StoryCommandOutline(StoryCommandHasContent):
    """
    A story command that represents the outline of a story.

    - 1st argument: outline content
    """

    @staticmethod
    def expected_type() -> StoryCommandType:
        return StoryCommandType.OUTLINE

    @property
    def content(self) -> str:
        return self.args[0]
