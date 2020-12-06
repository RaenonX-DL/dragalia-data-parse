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

    SELF_HP_GT = 1
    """
    Matches if the user's HP is > certain percent of the max HP.

    Condition value 1 is the HP% threshold.
    Condition value 2 does not have any effect.

    Condition value 1 = 40 means that the condition matches if the user's HP is > 40% of the max HP.
    """
    SELF_HP_LT = 37
    """
    Matches if the user's HP is < certain percent of the max HP.

    Condition value 1 is the HP% threshold.
    Condition value 2 does not have any effect.

    Condition value 1 = 40 means that the condition matches if the user's HP is < 40% of the max HP.
    """
    ON_QUEST_START = 15
    """
    This ability only triggers once when the quest starts.

    Condition value 1 and 2 are expected to be 0 since they are meaningless.
    """
    SELF_COMBO_COUNT = 21
    """
    Matches every time the combo count matches.

    Condition value 1 is the combo count to match.
    Condition value 2 does not have any effect.

    Condition value 1 = 30 means that the condition matches for every 30 combos.
    """
    SELF_HP_GTE = 60
    """
    Matches if the user's HP is >= certain percent of the max HP.

    Condition value 1 is the HP% threshold.
    Condition value 2 does not have any effect.

    Condition value 1 = 40 means that the condition matches if the user's HP is >= 40% of the max HP.
    """
    SELF_HP_LT_2 = 61
    """
    Matches if the user's HP is < certain percent of the max HP.

    Condition value 1 is the HP% threshold.
    Condition value 2 does not have any effect.

    Condition value 1 = 40 means that the condition matches if the user's HP is < 40% of the max HP.
    """

    @classmethod
    def _missing_(cls, _):
        return AbilityCondition.UNKNOWN
