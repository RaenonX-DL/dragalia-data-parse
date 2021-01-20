"""Enums for the actions."""
from enum import Enum

__all__ = ("AbilityTargetAction",)


class AbilityTargetAction(Enum):
    """
    Enums of the ability target action.

    This can be found in the field ``_TargetAction`` of ``ActionGrant``.

    The official definition can be found in ``Gluon.AbilityTargetAction`` of the metadata.
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

    @classmethod
    def _missing_(cls, _):
        return AbilityTargetAction.UNKNOWN
