"""Story command type enum."""
from enum import Enum
from typing import Any

__all__ = ("StoryCommandType",)


class StoryCommandType(Enum):
    """
    Story command type enum.

    There are NO official definitions available. However, except the placeholder for unknown command,
    the strings assigned to all other types of command actually exists.
    """

    UNKNOWN = "(unknown)"

    OUTLINE = "outline"
    """Outline of a story."""

    PRINT = "print"
    """A single text entry."""

    ADD_TEXT = "add_book_text"
    """Add text into a single screen. Current known use case is dragon story and poster-like message."""

    RUBY = "ruby"
    """Add text into a single screen. This is only used by JP. Contains a word with its Furigana."""

    WHITE_OUT = "WHITE_OUT_DEF"
    """White out the scene. Used for scene switching."""

    BLACK_OUT = "BLACK_OUT_DEF"
    """Black out the scene. Used for scene switching."""

    CHARA_SET = "CHARA_SET"
    """Set the character image of the speaker."""

    CHARA_SET_0 = "CHARA_SET_0"
    """Set the character image of the speaker. Difference between this and ``CHARA_SET`` is unknown."""

    CHARA_SET_3 = "CHARA_SET3"
    """Set 3 character images."""

    CHARA_KAMITE_SE = "CHARA_KAMITE_SE"
    """Set the character image of the speaker with a SE."""

    CHARA_SHIMOTE_SE = "CHARA_SHIMOTE_SE"
    """Set the character image of the speaker with a SE."""

    CHARA_SHIMOTE_POS_D = "CHARA_SHIMOTE_POS_d"
    """Set the character image of the speaker with some positional offset."""

    CHARA_SET_POS_0 = "CHARA_SET_POS_0"
    """
    Set the character image of the speaker with some positional offset.
    
    Difference between ``CHARA_SHIMOTE_POS_D`` is unknown.
    """

    PLAY_SOUND = "play_sound"
    """Play the voice."""

    @classmethod
    def _missing_(cls, value: Any) -> "StoryCommandType":
        return StoryCommandType.UNKNOWN
