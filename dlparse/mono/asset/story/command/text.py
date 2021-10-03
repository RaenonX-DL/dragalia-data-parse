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

    Note, in JP story, ``print`` command may have only 1 argument,
    which could either be a code-like string, or a part of a story content.
    Also, the 2nd argument might be a voice label.

    Regardless the language, the 1st appearance of this command in the same row is the speaker name/identifier.
    For CH/EN story, this is always the unit name;
    for JP story, this is the unit name in code which needs further processing to get its name.

    In the same row, the 2nd appearance and onward of this command is
    part of a story conversation (JP story) / conversation content (CHT/EN story).

    Also, JP story may contain this command without any argument.
    In this case, both ``speaker`` and ``content`` will return an empty string.
    """

    @property
    def speaker(self) -> str:
        """
        Name of the speaker of the text.

        This might be ``SYS`` for system message-like texts, or other names for NPC.

        For JP story, except the 1st occurrence of this command in the same row,
        this will be a part of the story content.

        Note that JP story may contain this command without any argument.
        In this case, both ``speaker`` and ``content`` will return an empty string.

        Also, for JP story, if the speaker name is an ID, it will NOT contain the story text.
        Otherwise, the speaker name will be the 1st argument (returned by this);
        part of the story conversation will be the 2nd argument (returned by ``content``).
        """
        if not self.args:
            return ""

        return self.args[0]

    @property
    def content(self) -> str:
        # Handle JP story containing empty argument
        if not self.args:
            return ""

        if len(self.args) < 2:
            return self.args[0]

        content = self.args[1]

        # Check if `content` is a voice label or not
        # If so, return the 1st argument; Otherwise, return the 2nd argument
        return self.args[0] if content.startswith("VO") else content
