"""Enums for the canceling actions."""
from enum import Enum

from .mixin import TranslatableEnumMixin

__all__ = ("SkillCancelAction",)


class SkillCancelAction(TranslatableEnumMixin, Enum):
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

    @property
    def translation_id(self) -> str:
        return f"SKILL_CANCEL_{self.name}"

    @staticmethod
    def get_all_translatable_members() -> list:
        return [
            SkillCancelAction.UNCLASSIFIED,
            SkillCancelAction.MOTION_ENDS,
            SkillCancelAction.ANY_ACTION,
            SkillCancelAction.ROLL,
            SkillCancelAction.FORMAL_JOACHIM_S1,
        ]

    @classmethod
    def _missing_(cls, _):
        return SkillCancelAction.UNCLASSIFIED
