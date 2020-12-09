"""Enums for the skill number."""
from enum import Enum

from dlparse.errors import InvalidSkillNumError

__all__ = ("SkillNumber",)


class SkillNumber(Enum):
    """
    Enums of the skill numbers. This is mainly for skill identifier entry.

    This is a custom enum. This may contains some sentinel values which is actually not a skill number.
    """

    NA = 0

    S1 = 1
    S2 = 2

    ABILITY = 10

    @property
    def repr(self) -> str:
        """
        Get the representation of the skill number.

        :raises InvalidSkillNumError: if the skill number does not have representation implemented yet
        """
        # Keeping the original `__repr__` implementation for enums to easier identify the enum while debugging
        if self == SkillNumber.S1:
            return "s1"

        if self == SkillNumber.S2:
            return "s2"

        if self == SkillNumber.ABILITY:
            return "ab"

        raise InvalidSkillNumError(self)

    @staticmethod
    def s1_s2_only(num: int) -> "SkillNumber":
        """
        Convert ``num`` to be either ``SkillNumber.NA``, ``SkillNumber.S1`` or ``SkillNumber.S2``.

        :raises InvalidSkillNumError: if `num` is invalid (not `0`, `1` or `2`)
        """
        if num == 0:
            return SkillNumber.NA

        if num == 1:
            return SkillNumber.S1

        if num == 2:
            return SkillNumber.S2

        raise InvalidSkillNumError(num)
