"""Story command class for ``CHARA_SET`` and ``CHARA_KAMITE_SE``."""
from dataclasses import dataclass

from .base import StoryCommandBase

__all__ = ("StoryCommandSetChara",)


@dataclass
class StoryCommandSetChara(StoryCommandBase):
    """
    Story command that sets the character image.

    This is applicable for the following types of command:
    - ``SET_CHARA``
    - ``CHARA_KAMITE_SE``
    """

    @property
    def image_code(self) -> str:
        """Image code of the speaker."""
        return self.args[3]
