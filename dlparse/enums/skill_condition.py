"""Conditions for the skill data entries."""
from enum import Enum

from dlparse.errors import EnumConversionError
from .affliction import Affliction

__all__ = ("SkillCondition",)


class SkillCondition(Enum):
    """Conditions for the skill data entries."""

    NONE = 0

    TARGET_POISONED = 101
    TARGET_BURNED = 102
    TARGET_FROZEN = 103
    TARGET_PARALYZED = 104
    TARGET_BLINDED = 105
    TARGET_STUNNED = 106
    TARGET_CURSED = 107
    TARGET_BOGGED = 109
    TARGET_SLEPT = 110
    TARGET_FROSTBITTEN = 111
    TARGET_FLASHBURNED = 112
    TARGET_CRASHWINDED = 113
    TARGET_SHADOWBLIGHTED = 114

    SELF_HP_1 = 201
    SELF_HP_FULL = 202
    SELF_BUFF_0 = 251
    SELF_BUFF_10 = 252
    SELF_BUFF_20 = 253
    SELF_BUFF_25 = 254
    SELF_BUFF_30 = 255
    SELF_BUFF_35 = 256
    SELF_BUFF_40 = 257
    SELF_BUFF_45 = 258
    SELF_BUFF_50 = 259

    @property
    def is_target_afflicted(self) -> bool:
        """If the condition needs the target to be afflicted."""
        # https://github.com/PyCQA/pylint/issues/2306
        return 100 <= self.value <= 199  # pylint: disable=comparison-with-callable

    @property
    def is_buff_boost(self):
        """If the condition is a buff boosted condition."""
        # https://github.com/PyCQA/pylint/issues/2306
        return 250 <= self.value <= 269  # pylint: disable=comparison-with-callable

    def to_affliction(self) -> Affliction:
        """
        Convert this :class:`SkillCondition` to :class:`Affliction`.

        :raises EnumConversionError: skill condition cannot be converted to affliction
        """
        if self not in TRANS_DICT_TO_AFFLICTION:
            raise EnumConversionError(self, self.__class__, Affliction)

        return TRANS_DICT_TO_AFFLICTION[self]

    def to_buff_count(self) -> int:
        """
        Convert this :class:`SkillCondition` to the actual count of buffs.

        :raises EnumConversionError: skill condition cannot be converted to buff count
        """
        if self not in TRANS_DICT_TO_BUFF_COUNT:
            raise EnumConversionError(self, self.__class__, "buff count")

        return TRANS_DICT_TO_BUFF_COUNT[self]

    @staticmethod
    def get_all_buff_count_conditions() -> list["SkillCondition"]:
        """Get a list of all buff count conditions."""
        return [
            SkillCondition.SELF_BUFF_0,
            SkillCondition.SELF_BUFF_10,
            SkillCondition.SELF_BUFF_20,
            SkillCondition.SELF_BUFF_25,
            SkillCondition.SELF_BUFF_30,
            SkillCondition.SELF_BUFF_35,
            SkillCondition.SELF_BUFF_40,
            SkillCondition.SELF_BUFF_45,
            SkillCondition.SELF_BUFF_50,
        ]

    @staticmethod
    def from_affliction(affliction: Affliction) -> "SkillCondition":
        """
        Convert ``affliction`` to :class:`SkillCondition`.

        :raises EnumConversionError: affliction cannot be converted to skill condition
        """
        if affliction not in TRANS_DICT_FROM_AFFLICTION:
            raise EnumConversionError(affliction, Affliction, SkillCondition)

        return TRANS_DICT_FROM_AFFLICTION[affliction]


TRANS_DICT_TO_AFFLICTION: dict[SkillCondition, Affliction] = {
    SkillCondition.TARGET_POISONED: Affliction.POISON,
    SkillCondition.TARGET_BURNED: Affliction.BURN,
    SkillCondition.TARGET_FROZEN: Affliction.FREEZE,
    SkillCondition.TARGET_PARALYZED: Affliction.PARALYZE,
    SkillCondition.TARGET_BLINDED: Affliction.BLIND,
    SkillCondition.TARGET_STUNNED: Affliction.STUN,
    SkillCondition.TARGET_CURSED: Affliction.CURSE,
    SkillCondition.TARGET_BOGGED: Affliction.BOG,
    SkillCondition.TARGET_SLEPT: Affliction.SLEEP,
    SkillCondition.TARGET_FROSTBITTEN: Affliction.FROSTBITE,
    SkillCondition.TARGET_FLASHBURNED: Affliction.FLASHBURN,
    SkillCondition.TARGET_CRASHWINDED: Affliction.CRASHWIND,
    SkillCondition.TARGET_SHADOWBLIGHTED: Affliction.SHADOWBLIGHT,
}
"""A :class:`dict` to convert :class:`SkillCondition` to :class:`Affliction`."""

TRANS_DICT_FROM_AFFLICTION: dict[Affliction, SkillCondition] = {
    Affliction.POISON: SkillCondition.TARGET_POISONED,
    Affliction.BURN: SkillCondition.TARGET_BURNED,
    Affliction.FREEZE: SkillCondition.TARGET_FROZEN,
    Affliction.PARALYZE: SkillCondition.TARGET_PARALYZED,
    Affliction.BLIND: SkillCondition.TARGET_BLINDED,
    Affliction.STUN: SkillCondition.TARGET_STUNNED,
    Affliction.CURSE: SkillCondition.TARGET_CURSED,
    Affliction.BOG: SkillCondition.TARGET_BOGGED,
    Affliction.SLEEP: SkillCondition.TARGET_SLEPT,
    Affliction.FROSTBITE: SkillCondition.TARGET_FROSTBITTEN,
    Affliction.FLASHBURN: SkillCondition.TARGET_FLASHBURNED,
    Affliction.CRASHWIND: SkillCondition.TARGET_CRASHWINDED,
    Affliction.SHADOWBLIGHT: SkillCondition.TARGET_SHADOWBLIGHTED,
}
"""A :class:`dict` to convert :class:`Affliction` to :class:`SkillCondition`."""

TRANS_DICT_TO_BUFF_COUNT: dict[SkillCondition, int] = {
    SkillCondition.SELF_BUFF_0: 0,
    SkillCondition.SELF_BUFF_10: 10,
    SkillCondition.SELF_BUFF_20: 20,
    SkillCondition.SELF_BUFF_25: 25,
    SkillCondition.SELF_BUFF_30: 30,
    SkillCondition.SELF_BUFF_35: 35,
    SkillCondition.SELF_BUFF_40: 40,
    SkillCondition.SELF_BUFF_45: 45,
    SkillCondition.SELF_BUFF_50: 50,
}
"""A :class:`dict` to convert :class:`SkillCondition` to the number of buff counts."""
