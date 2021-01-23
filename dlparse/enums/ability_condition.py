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

    Check ``notes/enums/AbilityCondition.md`` for the details of each member.

    Members with the certain prefixes has the following meaning:
    - ``EFF``: The ability will be effective as long as the condition matches
    - ``TRG``: The ability is triggered once when a certain condition matches
    """

    UNKNOWN = -1

    NONE = 0

    EFF_SELF_HP_GT = 1
    TRG_SELF_HP_LT_2 = 2
    EFF_IN_DRAGON = 5
    TRG_RECEIVED_BUFF_DEF = 8
    TRG_COMBO_COUNT_GTE = 9
    TRG_COMBO_COUNT_LT = 10
    TRG_SHAPESHIFTED_TO_DRAGON = 12
    TRG_SELF_HP_GT = 13
    TRG_SELF_HP_LT = 14
    TRG_QUEST_START = 15
    EFF_TARGET_OVERDRIVE = 16
    EFF_ENERGIZED = 18
    TRG_ENERGIZED = 19
    EFF_TARGET_AFFLICTED = 20
    TRG_COMBO_COUNT_DIV = 21
    TRG_INFLICTED_TARGET = 29
    TRG_GOT_HIT_WITH_AFFLICTION = 30
    TRG_SHAPESHIFTED_TO_DRAGON_2 = 31
    TRG_ENERGY_LV_UP = 36
    EFF_SELF_HP_LT = 37
    EFF_SELF_BUFFED_ACTION_COND = 48
    TRG_GOT_HIT = 49
    EFF_TARGET_DEBUFFED = 50
    TRG_SHAPESHIFT_COMPLETED = 51
    TRG_SELF_HP_GTE = 58
    TRG_SELF_HP_LTE = 59
    EFF_SELF_HP_GTE_2 = 60
    EFF_SELF_HP_LT_2 = 61
    EFF_IN_BUFF_ZONE = 88

    @property
    def is_shapeshifted_to_dragon(self) -> bool:
        """Check if the ability condition is "triggered when shapeshifted to dragon"."""
        return self in (AbilityCondition.TRG_SHAPESHIFTED_TO_DRAGON, AbilityCondition.TRG_SHAPESHIFTED_TO_DRAGON_2)

    @classmethod
    def _missing_(cls, _):
        return AbilityCondition.UNKNOWN
