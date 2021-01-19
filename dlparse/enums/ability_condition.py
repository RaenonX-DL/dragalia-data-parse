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

    EFF_SELF_HP_GTE = 1
    TRG_RECEIVED_BUFF_DEF = 8
    TRG_SELF_HP_LTE = 14
    TRG_QUEST_START = 15
    EFF_ENERGIZED = 18
    TRG_ENERGIZED = 19
    TRG_HIT_WITH_AFFLICTION = 30
    EFF_SELF_HP_LT = 37
    EFF_SELF_SPECIFICALLY_BUFFED = 48
    TRG_SHAPESHIFT_COMPLETED = 51
    EFF_SELF_HP_GTE_2 = 60
    EFF_SELF_HP_LT_2 = 61

    @classmethod
    def _missing_(cls, _):
        return AbilityCondition.UNKNOWN
