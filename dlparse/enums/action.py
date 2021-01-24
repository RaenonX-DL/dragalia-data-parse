"""Enums for the actions."""
from enum import Enum

from dlparse.errors import EnumConversionError
from .skill_num import SkillNumber

__all__ = ("AbilityTargetAction",)


class AbilityTargetAction(Enum):
    """
    Enums of the ability target action.

    This can be found in the field ``_TargetAction`` of ``ActionGrant``.

    The enum definition can be found in ``Gluon.AbilityTargetAction`` of the metadata.
    """

    UNKNOWN = -1

    NONE = 0

    AUTO = 1
    FORCE_STRIKE = 2
    SKILL_1 = 3
    SKILL_2 = 4
    SKILL_3 = 5
    SKILL_4 = 10
    SKILL_ALL = 6
    SKILL_1_HUMAN = 7
    SKILL_2_HUMAN = 8
    SKILL_3_HUMAN = 11
    SKILL_4_HUMAN = 12
    SKILL_1_DRAGON = 9

    @property
    def to_skill_num(self) -> SkillNumber:
        """
        Convert the current ability target action to skill number.

        :raises EnumConversionError: if the current ability target action cannot convert to skill number
        """
        if skill_num := _TRANS_DICT.get(self):
            return skill_num

        raise EnumConversionError(self, self.__class__, repr(SkillNumber))

    @classmethod
    def _missing_(cls, _):
        return AbilityTargetAction.UNKNOWN


_TRANS_DICT: dict[AbilityTargetAction, SkillNumber] = {
    AbilityTargetAction.SKILL_1: SkillNumber.S1,
    AbilityTargetAction.SKILL_2: SkillNumber.S2,
    AbilityTargetAction.SKILL_1_HUMAN: SkillNumber.S1,
    AbilityTargetAction.SKILL_2_HUMAN: SkillNumber.S2,
    AbilityTargetAction.SKILL_1_DRAGON: SkillNumber.S1_DRAGON,
}
