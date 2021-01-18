"""Enums for the canceling actions."""
from enum import Enum

__all__ = ("SkillCancelAction",)


class SkillCancelAction(Enum):
    """
    Enums of the skill canceling action.

    The value of this corresponds to the field ``_actionId`` of the action component ``ActionPartsActiveCancel``.
    """

    UNCLASSIFIED = -999

    # Not triggered by action ID
    MOTION_ENDS = -1

    # Misc
    ANY_ACTION = 0

    # Common action
    ROLL = 6

    # Specific action
    FORMAL_JOACHIM_S1 = 991060

    @classmethod
    def _missing_(cls, _):
        return SkillCancelAction.UNCLASSIFIED
