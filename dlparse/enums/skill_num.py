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

    S1_DRAGON = 11
    S2_DRAGON = 12

    ABILITY = 100

    @property
    def is_dragon_skill(self):
        """Check if the skill number is dragon skill."""
        return self in (self.S1_DRAGON, self.S2_DRAGON)

    @property
    def repr(self) -> str:
        """
        Get the representation of the skill number.

        :raises InvalidSkillNumError: if the skill number does not have representation implemented yet
        """
        # Keep the original `__repr__` implementation for enums to identify the enum while debugging easier
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
