"""Element enum."""

from enum import IntEnum

__all__ = ("Element",)


class Element(IntEnum):
    """
    Element enums used in the assets.

    This corresponds to the field ``_ElementalType`` in the character data asset.
    """

    UNKNOWN = -1

    N_A = 0
    FLAME = 1
    WATER = 2
    WIND = 3
    LIGHT = 4
    SHADOW = 5

    NO_ELEMENT = 99

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
