"""Enums for ability condition."""
from enum import Enum

__all__ = ("AbilityCondition",)


class AbilityCondition(Enum):
    """
    Enum class for ability condition in the assets.

    This corresponds to the field ``_ConditionType`` in the ability data asset.
    """

    UNKNOWN = -1

    NONE = 0

    SELF_HP_GTE = 60
    """
    Matches if the user's HP is >= certain percent of the max HP.

    Used for the situation where different effects will be applied under different threshold.

    Condition value = max HP threshold.
    Condition value 2 does not have any effect.

    Condition value = 40 means that the condition matches if the user's HP is >= 40% of the max HP.
    """
    SELF_HP_LT = 61
    """
    Matches if the user's HP is < certain percent of the max HP.

    Condition value = max HP threshold.
    Condition value 2 does not have any effect.

    Condition value = 40 means that the condition matches if the user's HP is < 40% of the max HP.
    """

    @classmethod
    def _missing_(cls, _):
        return AbilityCondition.UNKNOWN
