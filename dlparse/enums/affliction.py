"""Affliction enums."""
from enum import IntEnum

__all__ = ("Affliction",)


class Affliction(IntEnum):
    """Affliction enums used in the assets."""

    UNKNOWN = -1

    NONE = 0
    POISON = 1
    BURN = 2
    FREEZE = 3
    PARALYZE = 4
    BLIND = 5
    STUN = 6
    CURSE = 7
    BOG = 9
    SLEEP = 10
    FROSTBITE = 11
    FLASHBURN = 12
    CRASHWIND = 13
    SHADOWBLIGHT = 14

    UNKNOWN_1 = 99
    UNKNOWN_2 = 103
    UNKNOWN_3 = 198
    UNKNOWN_4 = 199
    UNKNOWN_5 = 201

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
