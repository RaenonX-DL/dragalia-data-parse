"""Elemental enums."""
from enum import Enum, Flag

from dlparse.errors import EnumConversionError

__all__ = ("Element", "ElementFlag")


class ElementFlag(Flag):
    """
    Elemental flags used in the master assets.

    This corresponds to the field ``_TargetElemental`` in the action condition asset.
    """

    FLAME = 1
    WATER = 2
    WIND = 4
    LIGHT = 8
    SHADOW = 16

    @property
    def is_effective(self) -> bool:
        """Check if the elemental flag is in effect."""
        return int(self.value) != 0


class Element(Enum):
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

    def to_flag(self) -> ElementFlag:
        """
        Convert this :class:`Element` to :class:`ElementFlag`.

        :raises EnumConversionError: if this :class:`Element` cannot convert to :class:`ElementFlag`
        """
        if self not in TRANS_DICT_TO_FLAG:
            raise EnumConversionError(self, Element, "Element flag")

        return TRANS_DICT_TO_FLAG[self]

    @classmethod
    def _missing_(cls, _):
        return cls.UNKNOWN

    @classmethod
    def from_flag(cls, elem_flag: ElementFlag) -> list["Element"]:
        """Convert the ``elem_flag`` to a list of corresponding elements."""
        return [element for element in cls.get_all_valid_elements() if element.to_flag() in elem_flag]

    @staticmethod
    def get_all_valid_elements() -> list["Element"]:
        """Get a list of all valid elements."""
        return [Element.FLAME, Element.WATER, Element.WIND, Element.LIGHT, Element.SHADOW]


TRANS_DICT_TO_FLAG: dict[Element, ElementFlag] = {
    Element.FLAME: ElementFlag.FLAME,
    Element.WATER: ElementFlag.WATER,
    Element.WIND: ElementFlag.WIND,
    Element.LIGHT: ElementFlag.LIGHT,
    Element.SHADOW: ElementFlag.SHADOW,
}
"""A :class:`dict` to convert :class:`Element` to :class:`ElementFlag`."""
