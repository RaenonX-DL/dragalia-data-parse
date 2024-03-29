"""Story command class for ``CHARA_SET`` and ``CHARA_KAMITE_SE``."""
from dataclasses import dataclass

from .base import StoryCommandHasImage

__all__ = ("StoryCommandSetChara",)


@dataclass
class StoryCommandSetChara(StoryCommandHasImage):
    """
    Story command that sets the character image.

    The 4th argument is the image code.

    This is applicable for the following types of command:
    - ``SET_CHARA``
    - ``CHARA_KAMITE_SE``
    """

    @property
    def image_code(self) -> str:
        """Image code of the speaker."""
        return self.args[3]
