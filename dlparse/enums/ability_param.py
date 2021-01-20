"""Enums for the status up (ability variant type 01 - StatusUp) parameter."""
from enum import Enum

from .buff_parameter import BuffParameter

__all__ = ("AbilityUpParameter",)


class AbilityUpParameter(Enum):
    """
    Ability status up parameters.

    This can be found in the ID-A field of the abiltity variants.
    """

    NONE = 0  # None
    HP = 1  # Hp
    ATK = 2  # Atk
    DEF = 3  # Def
    SP_RATE = 4  # Spr
    DP_RATE = 5  # Dpr
    DRAGON_TIME = 8  # DragonTime
    DAMAGE_REDUCTION = 9  # DamageCut
    ATK_SPEED = 10  # AttackSpeed
    DP_CONSUMPTION = 13  # ConsumeDpRate
    DRAGON_TIME_FINAL = 14  # FinalDragonTimeRate

    def to_buff_parameter(self) -> BuffParameter:
        """Convert the ability up parameter to the buff parameter."""
        return _TRANS_DICT[self]


_TRANS_DICT: dict[AbilityUpParameter, BuffParameter] = {
    AbilityUpParameter.HP: BuffParameter.HP_RAISE_BY_MAX,
    AbilityUpParameter.ATK: BuffParameter.ATK_PASSIVE,
    AbilityUpParameter.DEF: BuffParameter.DEF_PASSIVE,
    AbilityUpParameter.ATK_SPEED: BuffParameter.ASPD_PASSIVE,
    AbilityUpParameter.SP_RATE: BuffParameter.SP_RATE,
    AbilityUpParameter.DRAGON_TIME: BuffParameter.DRAGON_TIME,
    AbilityUpParameter.DRAGON_TIME_FINAL: BuffParameter.DRAGON_TIME_FINAL,
    AbilityUpParameter.DP_CONSUMPTION: BuffParameter.DP_CONSUMPTION
}
