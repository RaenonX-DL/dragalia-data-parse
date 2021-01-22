"""Enums for the ability unit type."""
from enum import Enum

__all__ = ("UnitType",)


class UnitType(Enum):
    """
    Unit type enum.

    Appears in the condition fields of the ability data and the EX ability data.

    Exact usage unknown.
    """

    UNKNOWN = -1

    NONE = 0
    CHARACTER = 1
    DRAGON = 2
    WYRMPRINT = 3
    WEAPON = 4
    SKILL = 5
    CHAINED_EX_ABILITY = 6
    EVENT_ABILITY = 7
    UNION_BONUS = 8

    @classmethod
    def _missing_(cls, _):
        return UnitType.UNKNOWN
