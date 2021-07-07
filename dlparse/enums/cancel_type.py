"""Enums of cancel action types."""
from enum import Enum

__all__ = ("SkillCancelType",)


class SkillCancelType(Enum):
    """
    Skill action cancel type.

    This can be found in the field ``_actionType`` of an ``ActionPartsActiveCancel`` action component.

    The official definition is located at ``Gluon/ActionPartsActiveCancel.cs``.
    """

    MOTION_ENDS = -2
    UNKNOWN = -1

    NONE = 0
    FS = 1  # Official name = `BurstAttack`
    AVOID = 2
    AVOID_FRONT = 3
    AVOID_BACK = 4

    @classmethod
    def _missing_(cls, _):
        return SkillCancelType.UNKNOWN
