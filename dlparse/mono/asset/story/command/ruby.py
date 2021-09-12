"""Story command class for ``ruby``."""
from dataclasses import dataclass

from .base import StoryCommandHasContent

__all__ = ("StoryCommandRuby",)


@dataclass
class StoryCommandRuby(StoryCommandHasContent):
    """
    A story command that prints a kanji with its furigana.

    This is only used by JP.

    - 1st argument: kanji
    - 2nd argument: corresponding furigana
    """

    @property
    def content(self) -> str:
        return self.args[0]
