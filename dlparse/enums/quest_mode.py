"""Enums for different mode of a quest."""
from enum import Enum

__all__ = ("QuestMode",)


class QuestMode(Enum):
    """
    Enum for the quest mode.

    The number corresponds to the field ``_QuestPlayModeType`` in quest data asset.

    The definition can be found in ``Gluon.QuestPlayModeType`` of the application metadata.
    """

    NONE = 0
    NORMAL = 1
    SOLO = 2
    MULTI = 3
    RANDOM_MATCH = 4
    RANDOM_MATCH_16 = 5
