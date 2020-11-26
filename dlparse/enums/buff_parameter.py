"""Buff parameter enum class."""
from enum import Enum

__all__ = ("BuffParameter",)


class BuffParameter(Enum):
    """
    Buff target parameter enum class.

    The number is arbitrarily defined (not appeared in the game asset).
    """

    # WARNING: The number should not be changed frequently because the changes need to be reflected at the frontend

    # region Common
    ATK = 101
    """ATK up. A value of 0.12 means ATK +12%."""
    DEF = 102
    """DEF up. A value of 0.12 means DEF +12%."""
    CRT_RATE = 103
    """Critical rate up. A value of 0.12 means CRT +12%."""
    CRT_DAMAGE = 104
    """Critical damage up. A value of 0.12 means CRT DMG +12%."""
    SKILL_DAMAGE = 105
    """Skill damage up. A value of 0.12 means SDMG +12%."""
    # endregion

    # SP Control
    SP_RATE = 201
    """Rate of SP gain. A value of 0.12 means SP +12%."""
    SP_GAIN = 202
    """Immediate SP gain. A value of 100 means get SP 100."""
    SP_CHARGE_PCT = 203
    """
    Immediately charges the SP by certain % of **ALL** skills.

    A value of 0.15 means to refill 15% SP of all skills.
    """
    SP_CHARGE_PCT_S1 = 204
    """
    Immediately charges the SP of **S1**.

    A value of 0.15 means to refill 15% SP of S1.
    """
    SP_CHARGE_PCT_S2 = 205
    """
    Immediately charges the SP of **S2**.

    A value of 0.15 means to refill 15% SP of S2.
    """
    # endregion
