"""Affliction enums."""
from enum import IntEnum

__all__ = ("Affliction",)


class Affliction(IntEnum):
    """
    Affliction enums used in the assets.

    This corresponds to the field ``_KillerState1``, ``_KillerState2`` and ``_KillerState3`` in
    the hit attribute asset.
    """

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

    AFFLICTED = 99

    DEF_DOWNED = 103
    BUFFED = 198
    DEBUFFED = 199

    BREAK_STATE = 201
