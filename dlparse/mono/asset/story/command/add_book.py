"""Story command class for ``add_book_text``."""
from dataclasses import dataclass

from .base import StoryCommandHasContent

__all__ = ("StoryCommandAddBook",)


@dataclass
class StoryCommandAddBook(StoryCommandHasContent):
    """A story command that prints content for dragon story or poster-like message."""

    @property
    def content(self) -> str:
        if not self.args:
            # Args list could be empty for some reason, no known effect of returning an empty string
            return ""

        return self.args[0]
