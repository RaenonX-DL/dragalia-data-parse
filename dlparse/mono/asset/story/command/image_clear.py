"""Story command class for the commands that clear the current image."""
from dataclasses import dataclass

from .base import StoryCommandBase

__all__ = ("StoryCommandImageClear",)


@dataclass
class StoryCommandImageClear(StoryCommandBase):
    """
    A story command that only clear the current image.

    This is used by ``CHARA_FADEOUT_DEF``.

    Despite the 1st argument being the image code of the image to clear,
    it's not useful for story command parsing.
    """
