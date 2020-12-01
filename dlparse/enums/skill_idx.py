"""Enum class for skill index."""
from enum import Enum

__all__ = ("SkillIndex",)


class SkillIndex(Enum):
    """
    Enums of the skill index.

    This can be found in the field ``_RecoverySpSkillIndex1`` and ``RecoverySpSkillIndex2`` of the hit attribute asset.
    """

    NOT_APPLICABLE = 0

    S1 = 1
    S2 = 2

    UNKNOWN_1 = 3  # BUF_191_SPC3_LV01 (3 / 3), BUF_192_SPC3_LV02 (3 / 3), BUF_196_SPC3_LV01 (3 / 3)

    USED_SKILL = 10  # BUF_192_SPC_LV02 (1 / 10), BUF_200_SPC_LV04 (1 / 10), BUF_191_SPC_LV01 (1 / 10)

    def __bool__(self):
        return self != self.NOT_APPLICABLE
