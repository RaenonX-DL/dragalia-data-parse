"""Story command class for character image setting commands with offset."""
from dataclasses import dataclass

from .base import StoryCommandHasImage

__all__ = ("StoryCommandPosDiff",)


@dataclass
class StoryCommandPosDiff(StoryCommandHasImage):
    """
    Story command that sets the character image.

    The 5th argument is the image code.

    This is applicable for the following types of command:
    - ``CHARA_SHIMOTE_POS_d``
    - ``CHARA_SET_POS_0``
    """

    @property
    def image_code(self) -> str:
        """Image code of the speaker."""
        return self.args[4]
