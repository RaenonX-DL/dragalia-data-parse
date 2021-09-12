"""Story command class for ``print``."""
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

    Note, in JP story, ``print`` command may have only 1 argument
    containing a code-like string which is not a story content.
    """

    @property
    def speaker(self) -> str:
        """
        Name of the speaker of the text.

        This might be ``SYS`` for system message-like texts, or other names for NPC.
        """
        return self.args[0]

    @property
    def content(self) -> str:
        if len(self.args) < 2:
            return ""

        return self.args[1]
