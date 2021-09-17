"""Story command class for ``CHARA_SET``."""
from dataclasses import dataclass

from .base import StoryCommandBase

__all__ = ("StoryCommandSetChara",)


@dataclass
class StoryCommandSetChara(StoryCommandBase):
    """Story command that sets the character image."""

    @property
    def image_code(self) -> str:
        """Image code of the speaker."""
        return self.args[3]
