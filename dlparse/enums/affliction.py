"""Affliction enums."""
from enum import IntEnum

__all__ = ("Affliction",)


class Affliction(IntEnum):
    """Affliction enums used in the assets."""

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
