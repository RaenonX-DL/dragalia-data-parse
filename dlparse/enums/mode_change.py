"""Enums of the mode change type."""
from enum import Enum

__all__ = ("ModeChangeType",)


class ModeChangeType(Enum):
    """
    Enum for the mode change type.

    The number corresponds to the field ``_ModeChangeType`` in chara data asset.

    The definition can be found in ``Gluon.PlayerCharacter.ModeChangeType`` in the metadata.
    """

    UNKNOWN = -1

    NONE = 0
    SKILL = 1
    BUTTON = 2  # Mitsuba, Valerio, etc.
    UNIQUE_TRANSFORM = 3  # Bellina, P5S units, etc.
    BUFF_STACK = 4
    ABILITY = 5

    @classmethod
    def _missing_(cls, _):
        return ModeChangeType.UNKNOWN
