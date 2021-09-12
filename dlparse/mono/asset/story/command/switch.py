"""Story command class for ``BLACK_OUT_DEF`` or ``WHITE_OUT_DEF``."""
from dataclasses import dataclass

from .base import StoryCommandBase

__all__ = ("StoryCommandThemeSwitch",)


@dataclass
class StoryCommandThemeSwitch(StoryCommandBase):
    """
    A story command that switches the theme by either black out or white out.

    No arguments available for this commmand.
    """
