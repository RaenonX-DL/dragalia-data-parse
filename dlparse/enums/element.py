"""Elemental enums."""
from enum import Enum, Flag

from dlparse.errors import EnumConversionError
from .buff_parameter import BuffParameter

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

    @property
    def elements(self) -> list["Element"]:
        """Get a list of effective elements of this flag."""
        return [elem for elem in Element.get_all_valid_elements() if elem.to_flag() in self]


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

    @property
    def is_valid(self) -> bool:
        """
        Check if the element is valid.

        A valid element must be one of Flame, Water, Wind, Light, or Shadow.
        """
        return self in self.get_all_valid_elements()

    def to_flag(self) -> ElementFlag:
        """
        Convert this :class:`Element` to :class:`ElementFlag`.

        :raises EnumConversionError: if this :class:`Element` cannot convert to :class:`ElementFlag`
        """
        if self not in _TRANS_DICT_TO_FLAG:
            raise EnumConversionError(self, Element, "Element flag")

        return _TRANS_DICT_TO_FLAG[self]

    def to_elem_dmg_up(self) -> BuffParameter:
        """
        Convert this :class:`Element` to the corrsponding damage buff :class:`BuffParameter`.

        :raises EnumConversionError: if this element does not correspond to any elemental damage buff
        """
        if self not in _TRANS_DICT_TO_ELEM_DMG:
            raise EnumConversionError(self, Element, "Element damage buff parameter")

        return _TRANS_DICT_TO_ELEM_DMG[self]

    def to_elem_res_up(self) -> BuffParameter:
        """
        Convert this :class:`Element` to corrsponding damage resistance :class:`BuffParameter`.

        :raises EnumConversionError: if this element does not correspond to any elemental resistance buff
        """
        if self not in _TRANS_DICT_TO_ELEM_RES:
            raise EnumConversionError(self, Element, "Element damage resistance parameter")

        return _TRANS_DICT_TO_ELEM_RES[self]

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


_TRANS_DICT_TO_FLAG: dict[Element, ElementFlag] = {
    Element.FLAME: ElementFlag.FLAME,
    Element.WATER: ElementFlag.WATER,
    Element.WIND: ElementFlag.WIND,
    Element.LIGHT: ElementFlag.LIGHT,
    Element.SHADOW: ElementFlag.SHADOW,
}
"""A :class:`dict` to convert :class:`Element` to :class:`ElementFlag`."""

_TRANS_DICT_TO_ELEM_DMG: dict[Element, BuffParameter] = {
    Element.FLAME: BuffParameter.FLAME_ELEM_DMG_UP,
    Element.WATER: BuffParameter.WATER_ELEM_DMG_UP,
    Element.WIND: BuffParameter.WIND_ELEM_DMG_UP,
    Element.LIGHT: BuffParameter.LIGHT_ELEM_DMG_UP,
    Element.SHADOW: BuffParameter.SHADOW_ELEM_DMG_UP,
}
"""A :class:`dict` to convert :class:`Element` to its corresponding elemental damage up buff parameter."""

_TRANS_DICT_TO_ELEM_RES: dict[Element, BuffParameter] = {
    Element.FLAME: BuffParameter.RESISTANCE_FLAME,
    Element.WATER: BuffParameter.RESISTANCE_WATER,
    Element.WIND: BuffParameter.RESISTANCE_WIND,
    Element.LIGHT: BuffParameter.RESISTANCE_LIGHT,
    Element.SHADOW: BuffParameter.RESISTANCE_SHADOW,
}
"""A :class:`dict` to convert :class:`Element` to its corresponding elemental damage resistance buff parameter."""
