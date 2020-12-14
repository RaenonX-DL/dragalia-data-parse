"""
Enums for ability condition.

Check ``notes/enums/AbilityCondition.md`` for more details.
"""
from enum import Enum

__all__ = ("AbilityCondition",)


class AbilityCondition(Enum):
    """
    Enum class for ability condition in the assets.

    This corresponds to the field ``_ConditionType`` in the ability data asset.

    Check ``notes/enums/AbilityCondition.md`` for more details.
    """

    UNKNOWN = -1

    NONE = 0

    SELF_HP_GT = 1
    """
    Match if the user's HP is > certain percent of the max HP.

    Condition value 1 = 40 means that the condition matches if the user's HP is > 40% of the max HP.
    """
    QUEST_START = 15
    """Apply all the effects once at the beginning of the quest."""
    ENERGIZED = 18
    """Match if the user is energized."""
    ENERGIZED_MOMENT = 19
    """
    Match if the user is energized.

    Note that the difference between `ENERGIZED` is that the effect of `ENERGIZED` will stay as long as
    the user is energized, whereas the effect of `ENERGIZED_ONCE` will be granted once the user is energized.
    """
    SELF_HP_LT = 37
    """
    Match if the user's HP is < certain percent of the max HP.

    Condition value 1 = 40 means that the condition matches if the user's HP is < 40% of the max HP.
    """
    SELF_HP_GTE = 60
    """
    Match if the user's HP is > certain percent of the max HP.

    Condition value 1 = 40 means that the condition matches if the user's HP is > 40% of the max HP.
    """
    SELF_HP_LT_2 = 61
    """
    Match if the user's HP is < certain percent of the max HP.

    Condition value 1 = 40 means that the condition matches if the user's HP is < 40% of the max HP.
    """

    @classmethod
    def _missing_(cls, _):
        return AbilityCondition.UNKNOWN
