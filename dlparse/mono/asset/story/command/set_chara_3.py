"""Story command class for ``CHARA_SET3``."""
from dataclasses import dataclass

from .base import StoryCommandHasImage

__all__ = ("StoryCommandSetChara3",)


@dataclass
class StoryCommandSetChara3(StoryCommandHasImage):
    """
    Story command that sets 3 character images. This class takes the middle (2nd) one as default.

    The 3rd argument is the 1st character image.
    The 7th argument is the 2nd character image.
    The 11th argument is the 3rd character image.

    This is applicable for the following types of command:
    - ``CHARA_SET3``
    """

    @property
    def image_code(self) -> str:
        """Image code of the speaker."""
        return self.args[6]
