"""Enums for skill chain condition."""
from enum import Enum

from dlparse.errors import AppValueError

__all__ = ("SkillChainCondition",)


class SkillChainCondition(Enum):
    """
    Enums of the skill chain condition.

    This corresponds to the field ``_ActivateCondition`` in the skill chain data asset.
    """

    UNKNOWN = -1

    NONE = 0
    TARGET_HAS_BUFF = 1
    TARGET_BK_STATE = 2

    @property
    def repr(self) -> str:
        """Get the representation of the chain condition."""
        # Keep the original `__repr__` implementation for enums to identify the enum while debugging easier
        if self == SkillChainCondition.NONE:
            return "none"

        if self == SkillChainCondition.TARGET_HAS_BUFF:
            return "target_buffed"

        if self == SkillChainCondition.TARGET_BK_STATE:
            return "target_bk"

        raise AppValueError(f"Representation for `{self}` not available")

    @classmethod
    def _missing_(cls, _):
        return SkillChainCondition.UNKNOWN
